---
name: acuity-eval-report
description: Generate an evaluation conversion report from Acuity Scheduling — counting evaluations per provider calendar, pulling client intake data (DOB, referral source, etc.), and determining whether each eval converted into a package purchase. Use this skill whenever the user mentions evaluation reports, eval counts, conversion rates, eval tracking, "how many evals", "missed opportunities", package conversion, or any request to audit or report on PT Evaluations from Acuity. Also trigger when the user asks about new patient intake data, eval-to-package pipeline, or provider performance metrics from Acuity.
---

# Acuity Evaluation Report Skill

Generate a per-provider evaluation conversion table from Acuity Scheduling for any date range. The output includes eval count, client name, date of birth, and package purchased (or "Missed Opportunity").

---

## Prerequisites — Verify Before Starting

### Required MCP Connectors

Before executing ANY step, confirm these are enabled. If missing, STOP and give the user numbered steps to enable them.

| Connector | Where to Enable | What It's Used For |
|---|---|---|
| **Zapier MCP** | Claude.ai → Settings → Connected Apps → Zapier | All Acuity API calls route through Zapier's `acuity_scheduling_api_request_beta` action |

### Required Zapier Action

Inside the Zapier MCP, the following action must be configured:

- **Acuity Scheduling: API Request (Beta)** — This is the raw HTTP action that lets Claude call any Acuity API endpoint with authentication already handled.

If the user has never used this Zapier action before, they may need to:
1. Go to https://actions.zapier.com
2. Click **"Add a new action"**
3. Search for **"Acuity Scheduling"**
4. Select **"API Request (Beta)"**
5. Connect their Acuity account (API key + User ID)
6. Save and confirm

---

## Execution Protocol

### PHASE 1: Gather Inputs from User

Ask the user (one question at a time, multiple choice):

**Q1: Date range?**
- A) Month-to-date
- B) Year-to-date
- C) Custom range (I'll specify)
- D) Last quarter

**Q2: Which provider calendars?**
- A) All calendars (I'll pull the list)
- B) Specific provider(s) — I'll name them
- C) Just mine

**Q3: What columns do you want in the final table?**
- A) Standard: Date, Client Name, DOB, Package Purchased
- B) Extended: Standard + Referral Source, Body Region, Goal
- C) Custom — I'll tell you which intake fields

---

### PHASE 2: Pull Calendar IDs

**API Call:**
```
GET https://acuityscheduling.com/api/v1/calendars
```

**What to extract:** `id` and `name` for each calendar.

**Output format to hold in memory:**
```
Calendar Map:
- {calendar_name_1} → ID: {id_1}
- {calendar_name_2} → ID: {id_2}
- {calendar_name_3} → ID: {id_3}
```

Present the calendar list to the user and confirm which ones to include.

---

### PHASE 3: Identify Evaluation Appointment Types

**API Call:**
```
GET https://acuityscheduling.com/api/v1/appointment-types
```

**What to extract:** Any appointment type where the `name` contains the word **"Evaluation"** (case-insensitive).

**Store the matching type IDs.** These are the filter criteria for the next step.

**Known evaluation types at Project Performance (may change over time):**
- PT Evaluation - $99 - Promo (ID: 78878996)
- PT Evaluation (ID: 79164173)
- PT Evaluation - $129 - Promo (ID: 89759325)

> **IMPORTANT:** Always re-pull this list. Do NOT hardcode IDs — Brandon may add/rename/retire evaluation types at any time.

---

### PHASE 4: Pull All Appointments per Calendar in Date Range

For EACH calendar the user selected, make this call:

**API Call:**
```
GET https://acuityscheduling.com/api/v1/appointments?calendarID={CALENDAR_ID}&minDate={START_DATE}&maxDate={END_DATE}&max=500&direction=ASC
```

**Parameters:**
- `calendarID` = the ID from Phase 2
- `minDate` = start of date range (format: `YYYY-MM-DD`)
- `maxDate` = end of date range (format: `YYYY-MM-DD`)
- `max=500` = maximum results per call
- `direction=ASC` = chronological order

**What to extract per appointment:**
- `id` (appointment ID)
- `appointmentTypeID`
- `type` (the appointment type name)
- `date`
- `time`
- `firstName`
- `lastName`
- `calendar` (calendar/provider name)

**Filter logic:** Only keep appointments where the `type` name contains "Evaluation" (matching the types from Phase 3).

**Store as the Evaluations List:**
```
Provider: {calendar_name}
Eval #1: {date} | {firstName} {lastName} | Appt ID: {id}
Eval #2: {date} | {firstName} {lastName} | Appt ID: {id}
...
```

**Pagination note:** If a provider has more than 500 appointments in the range, make additional calls using `minDate` set to the day after the last appointment returned. This is rare for typical date ranges but important for year-long pulls.

---

### PHASE 5: Pull Intake Form Data (DOB + Optional Fields)

For EACH evaluation appointment, pull the full appointment details to get the intake form responses.

**API Call:**
```
GET https://acuityscheduling.com/api/v1/appointments/{APPOINTMENT_ID}
```

**What to extract from the response:**
- Navigate into `forms[]` → `values[]`
- Find the field where `name` = `"Date of Birth (MM/DD/YY)"`
- Extract the `value`

**If the user requested Extended columns (Phase 1, Q3 = B), also extract:**
- `"How did you hear about us? (Who referred you?)"` → Referral Source
- `"What body region(s) are we focusing on?"` → Body Region
- `"What is your number one goal for physical therapy?"` → Goal

**Edge case — blank forms:** Some clients never fill out the intake form. If the DOB field (and all other fields) return empty strings, note it as **"Not filled out"** in the table and flag it to the user as a follow-up item.

**DOB formatting:** Clients enter DOB inconsistently. Normalize all DOBs to `MM/DD/YYYY` (4-digit year). Common input patterns:
- `03/28/92` → `03/28/1992`
- `04/20/1998` → `04/20/1998` (already correct)
- `081697` → `08/16/1997` (no slashes — parse as MMDDYY)

---

### PHASE 6: Determine Package Conversion

This is the key business logic. For each eval client, determine if they purchased a session package.

#### Method A — Follow-Up Session Check (Fast, Preferred)

Using the full appointment list already pulled in Phase 4, check if the eval client has **any PT Session (non-eval) appointments booked AFTER their evaluation date** on the same provider's calendar.

**Logic:**
```
For each eval client:
  Search the full appointment list for:
    - Same firstName + lastName
    - appointmentTypeID ≠ any Evaluation type
    - date > eval date
  If found → CONVERTED (has follow-up sessions)
  If not found → Check Method B or mark as "Missed Opportunity"
```

> **Note:** This method catches most conversions but may miss clients who were transferred to a different provider's calendar after their eval. If accuracy is critical, also run Method B.

#### Method B — Certificate/Package Lookup (Definitive, Slower)

For clients who converted (or to double-check), look up their actual package:

**Step 1: Get the client's email**
```
GET https://acuityscheduling.com/api/v1/appointments/{APPOINTMENT_ID}
```
Extract: `email`

**Step 2: Search certificates by email**
```
GET https://acuityscheduling.com/api/v1/certificates?email={CLIENT_EMAIL}
```

**What to extract:**
- `name` (the package/product name)
- `remainingCounts` → remaining appointments

If a certificate is found → record the package name.
If no certificate found → **"Missed Opportunity"**

**Edge cases:**
- Client purchased a package but used a different email → will show as "Missed Opportunity" via this method. Method A (follow-up check) catches these.
- Client has MULTIPLE certificates → use the most recent one (highest certificate ID).
- Eval happened today → mark as **"⏳ Today — TBD"** since they haven't had time to purchase yet.

#### Recommended Approach
1. Run Method A first (it's free — you already have the data)
2. For confirmed conversions, run Method B to get the exact package name
3. For non-conversions from Method A, optionally run Method B as a double-check

---

### PHASE 7: Build the Output Table

Assemble everything into a markdown table, grouped by provider:

```
## {Provider Name}'s Evaluations — {Date Range}

| # | Eval Date | Client | Date of Birth | Package Purchased |
|---|-----------|--------|---------------|-------------------|
| 1 | {date}    | {name} | {DOB}         | {package or Missed Opportunity} |
```

**Summary stats to include below each provider's table:**
- Total evaluations: {count}
- Converted: {count} ({percentage}%)
- Missed Opportunities: {count}
- Pending (eval today): {count}

**If multiple providers, also include a combined summary:**
```
## Combined Summary
- Total evaluations across all providers: {count}
- Overall conversion rate: {percentage}%
- Top converting provider: {name} at {percentage}%
```

---

## API Reference (Quick Lookup)

| Endpoint | Method | Purpose |
|---|---|---|
| `/api/v1/calendars` | GET | List all provider calendars |
| `/api/v1/appointment-types` | GET | List all appointment types |
| `/api/v1/appointments?calendarID={}&minDate={}&maxDate={}&max=500&direction=ASC` | GET | Pull appointments for a calendar in a date range |
| `/api/v1/appointments/{id}` | GET | Get full appointment details + intake form data |
| `/api/v1/certificates?email={}` | GET | Look up packages purchased by client email |

All calls go through: `Zapier:acuity_scheduling_api_request_beta`
- `method`: `GET`
- `url`: the full URL above
- `output_hint`: describe what you want returned (e.g., "Return firstName, lastName, email, and all form field names and values")

---

## Scaling Notes

### Adding a New Provider
When Brandon hires a new PT or contractor:
1. They get added as a new Calendar in Acuity
2. This skill automatically picks them up in Phase 2 (calendar list pull)
3. No changes needed — just select their calendar when prompted

### Running for a Single Provider
If the user says "just Jeremy's evals" — skip the other calendars in Phase 4. Everything else stays the same.

### Running Monthly vs. Quarterly vs. Yearly
Just change the `minDate` and `maxDate` parameters. The 500-appointment limit per call handles up to ~2 months of a busy calendar. For longer ranges, paginate (see Phase 4 pagination note).

### Extending the Table with More Intake Fields
All intake form fields are available in the Phase 5 API response. To add a new column, just extract the matching field name from `forms[].values[]`. Common fields available:
- Date of Birth (MM/DD/YY)
- How did you hear about us? (Who referred you?)
- What are you coming in for today?
- What is your number one goal for physical therapy?
- What body region(s) are we focusing on?
- Have you had physical therapy before?
- Please check all providers you have seen for this injury/problem

---

## Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| API returns empty results | Wrong calendar ID or date range | Re-pull calendar list and verify IDs |
| DOB field is blank | Client didn't fill out intake form | Flag to user — needs manual follow-up |
| Certificate lookup returns nothing but client has sessions | Package purchased under different email, or was entered manually in Acuity without a certificate | Use Method A (follow-up check) as the primary signal |
| More than 500 appointments in range | High-volume calendar or long date range | Paginate — make additional calls starting from the day after the last result |
| Tool call fails with "not loaded" error | Zapier MCP tool needs to be re-loaded in the session | Run `tool_search` with query "acuity scheduling api request" to reload the tool definition |
