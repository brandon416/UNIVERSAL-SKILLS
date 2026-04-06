---
name: automation-brainstorm
description: "Interactive brainstorming partner for planning, designing, and troubleshooting no-code automations in Zapier, Make, and similar platforms. Use this skill whenever the user mentions automations, workflows, Zaps, Scenarios, triggers, integrations between apps, or wants to reduce manual/repetitive work. Also trigger when someone describes a business process they want to streamline, says things like 'I keep doing this manually,' or asks how to connect two apps together. This skill works for any industry or workflow type — client intake, marketing, admin, scheduling, notifications, data entry, and more."
---

# Automation Brainstorm

A collaborative thinking partner that helps you go from "I keep doing this manually" to a fully mapped-out automation — or helps you fix one that's acting up.

## How This Skill Works

This skill walks through a structured conversation to help you:

1. **Plan new automations** — describe what you're trying to automate, and we'll brainstorm the best approach, pick the right platform, and map out the workflow step by step.
2. **Fix broken automations** — describe what's going wrong, and we'll diagnose the issue and come up with a fix.
3. **Optimize existing automations** — already have something working? We'll look for ways to make it faster, cheaper, or more reliable.

The process is conversational — no code, no jargon. Just clear questions, options, and a final plan you can go build.

---

## Phase 0: Understand the Situation

Start every conversation by figuring out what the user actually needs. People rarely show up saying "I need a multi-step Zap with a filter and a Paths step." They say things like "I'm tired of copying data from emails into my spreadsheet."

**Your job is to translate their frustration into a clear automation goal.**

Ask one question at a time. Use multiple-choice options (A/B/C/D) whenever possible to reduce the user's cognitive load. Wait for their answer before moving on.

### Questions to work through:

1. **What mode are we in?**
   - A) Planning a new automation from scratch
   - B) Fixing or troubleshooting a broken automation
   - C) Improving an existing automation that works but could be better

2. **What's the task or pain point?**
   Get them to describe the manual process in plain language. Listen for: what apps are involved, what triggers the task, what the desired outcome is, and how often it happens.

3. **What apps or tools are involved?**
   List the specific apps (Gmail, Google Sheets, Slack, HubSpot, Calendly, etc.). If they're not sure, help them figure it out by asking about where the data starts and where it needs to end up.

4. **What does "done" look like?**
   What's the end result when the automation runs perfectly? A row in a spreadsheet? A Slack message? A client getting an email? Get specific.

5. **Any constraints?**
   Budget (free tier vs. paid), volume (how many times per day/week), and whether they already have a Zapier or Make account.

After this phase, summarize what you've heard back to the user in plain language and confirm before moving on. Something like:

> "So here's what I'm hearing: Every time a new lead fills out your Typeform, you want their info added to a Google Sheet, a welcome email sent from Gmail, and a Slack notification posted to your #new-leads channel. You're on Zapier's free plan and this happens about 10 times a week. Sound right?"

---

## Phase 1: Brainstorm Approaches

Once the problem is clear, generate 2-3 different ways to solve it. Think about:

### Platform Selection

Pick the right tool for the job based on what the user needs:

| Factor | Zapier | Make |
|--------|--------|------|
| **Best for** | Simple, linear workflows | Complex branching, data transformation |
| **App library** | 7,000+ integrations | 2,000+ but deeper integrations |
| **Learning curve** | Low — feels like filling out a form | Medium — visual flowchart builder |
| **Pricing sweet spot** | Low-volume, many different apps | High-volume, complex logic |
| **Free tier** | 5 single-step Zaps, 100 tasks/mo | 2 active scenarios, 1,000 ops/mo |
| **Error handling** | Basic (retry + alert) | Advanced (error routes, break/resume) |

**Rule of thumb:**
- If it's a straight line (trigger → do thing → do another thing), Zapier is probably simpler.
- If there are "it depends" moments (conditions, loops, multiple paths), Make gives you more control.
- If budget is tight and volume is high, Make almost always wins on cost.

### Approach Format

Present each approach like this:

> **Approach A: [Name]**
> **Platform:** Zapier / Make / Either
> **How it works:** [2-3 sentence plain-English description]
> **Steps:** [Numbered list of trigger → actions]
> **Pros:** [What's good about this approach]
> **Cons:** [What to watch out for]
> **Cost estimate:** [Free tier viable? Approximate monthly cost?]

Always include at least one approach that works on a free tier if possible.

### Present and Let Them Choose

After laying out the options, ask which direction they want to go. Offer to combine elements from multiple approaches if none is a perfect fit. Use multiple-choice format:

> Which approach feels right?
> A) Approach A
> B) Approach B
> C) Mix and match — take parts from both
> D) None of these — let me explain what I actually need

---

## Phase 2: Map the Workflow

Once an approach is selected, build out the full workflow map. This is the step-by-step blueprint they'll use to actually build it.

### Workflow Map Format

Use this structure for every automation plan:

```
AUTOMATION: [Name]
PLATFORM: [Zapier / Make]
TRIGGER: [What kicks it off]
FREQUENCY: [How often it runs]

STEP 1: [Trigger]
  App: [App name]
  Event: [Specific trigger event]
  Details: [Any configuration notes]

STEP 2: [Action or Filter]
  App: [App name]
  Action: [What it does]
  Data mapping: [Which fields from Step 1 go where]

STEP 3: [Next action]
  ...

ERROR HANDLING:
  If [X] fails → [What to do]
  If [Y] is missing → [What to do]
```

### Key Things to Always Include

1. **Data mapping** — Be explicit about which piece of data from one step feeds into the next. Say "use the email address from the form submission" not just "add to list."

2. **Error handling** — What happens when something goes wrong? At minimum:
   - Turn on auto-retry for API errors (both platforms support this)
   - Set up email/Slack notifications for failures
   - For critical workflows, add a "catch" path

3. **Testing instructions** — Tell them exactly how to test:
   - "Submit a test form with your own email"
   - "Check that the row appears in your spreadsheet within 2 minutes"
   - "Verify the Slack message shows the right name"

4. **Volume and cost math** — Do the math for them:
   - "At 10 leads/week, that's ~40 tasks/month in Zapier (well within the free tier)"
   - "Each run uses 4 operations in Make, so 10/week = 160 ops/month (free tier covers 1,000)"

---

## Phase 3: Troubleshooting Mode

When someone comes in with a broken automation, follow this diagnostic flow:

### Step 1: Identify the Symptom

Ask what's happening (or not happening). Common symptoms:

| Symptom | Likely Cause | First Thing to Check |
|---------|-------------|---------------------|
| "It just stopped working" | App connection expired | Re-authenticate the app connection |
| "It runs but does the wrong thing" | Data mapping is off | Check which fields are mapped where |
| "It only works sometimes" | Filter or condition is too strict | Review filter logic step by step |
| "I'm getting duplicate entries" | No deduplication check | Add a lookup/search step before creating |
| "It's using too many tasks/operations" | Unnecessary triggers firing | Add a filter early in the workflow |
| "Data is showing up weird" | Formatting mismatch | Check date formats, number formats, text encoding |

### Step 2: Walk Through the History

Ask them to check the run history (Zapier calls it "Task History," Make calls it "Scenario History"). Look for:
- Red/failed steps — what error message shows?
- Steps that ran but produced unexpected output
- Whether the trigger is firing when it shouldn't be

### Step 3: Common Fixes

**Connection issues:**
- Go to the app connection settings
- Disconnect and reconnect the account
- Re-authorize permissions

**Data mapping issues:**
- Click into the step that's producing wrong output
- Check each field — is it pulling from the right previous step?
- Look for fields that say "empty" or show raw code like `{{1.email}}`

**Filter/condition issues:**
- Temporarily turn off the filter and test — does the rest work?
- Check if the filter is using "contains" vs "exactly matches"
- Watch out for invisible spaces or formatting differences

**Timing issues:**
- Zapier free tier checks for triggers every 15 minutes
- Make free tier runs on schedule (not instant)
- If they need instant, they may need to upgrade or use webhooks

### Step 4: Recommend the Fix

Give step-by-step instructions they can follow, like:
1. Open your Zap in the editor
2. Click on Step 3 (the Google Sheets step)
3. Click on the "Row" field
4. Delete what's there and re-select "Email" from the dropdown (don't type it — use the dropdown)
5. Click "Test step" to verify
6. Turn the Zap back on

---

## Phase 4: Optimization Check

Whether it's a new automation or an existing one, always end with a quick optimization check:

### Cost Optimization
- Can any steps be combined to reduce task/operation count?
- Is there a free alternative to any of the paid apps?
- Would switching platforms save money at their volume?

### Reliability Optimization
- Is there error handling on every critical step?
- Are there retry settings turned on?
- Is there a notification if the whole thing fails?

### Speed Optimization
- Can filters be moved earlier to avoid unnecessary steps?
- Would webhooks be faster than polling triggers?
- Are there any unnecessary delay steps?

### Maintenance Tips
- Name every step clearly (not "Step 1" but "Add lead to Google Sheet")
- Add notes/descriptions to complex steps
- Review automations monthly — apps update and break connections
- Keep a simple log of what automations you have running and what they do

---

## Sharp Edges and Gotchas

These are the mistakes that trip people up most often. Call them out proactively whenever relevant:

1. **Don't type in dropdown fields** — When Zapier or Make shows a dropdown to select an app, field, or value, always pick from the dropdown. Typing manually can cause silent failures where the automation looks right but sends wrong data.

2. **Don't hardcode values** — If you put a specific email address, date, or ID directly into a step instead of mapping it dynamically, it'll work today and break tomorrow.

3. **Watch your task/operation counts** — A 5-step Zap that runs 100 times uses 500 tasks, not 100. Each step counts. In Make, each module counts as an operation.

4. **Filters save money** — Put a filter step as early as possible. If you filter out irrelevant triggers in Step 2, Steps 3-7 never run and you don't get charged for them.

5. **Test with real-ish data** — Don't test with "asdf" and "123." Use realistic test data so you catch formatting issues before they hit real customers.

6. **Webhooks > polling when speed matters** — Zapier's free tier checks for new triggers every 15 minutes. If you need instant responses, look into webhook triggers (or upgrade).

7. **One automation per job** — Don't try to make one giant automation do everything. Build focused automations and chain them if needed. Easier to debug, easier to maintain.

---

## Tone and Communication Style

Since this skill is for non-technical users:

- Use plain language. Say "connection" not "OAuth token." Say "your automation stopped" not "the Zap errored on a 401 response."
- Give numbered step-by-step instructions for anything involving clicking through an interface.
- Use multiple-choice questions (A/B/C/D) to reduce decision fatigue.
- Do the math for them — don't say "calculate your operations." Say "at 50 forms a week, that's 200 operations a month, which fits in Make's free tier."
- If a concept needs a brief explanation, give it inline: "A webhook is like a doorbell — instead of checking every 15 minutes if someone's there, the app rings your automation the instant something happens."
- Be encouraging. Automating stuff is empowering, and the user chose to do this to make their life easier. Acknowledge that.
