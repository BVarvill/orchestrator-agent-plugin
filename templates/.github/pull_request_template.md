<!-- Title: say the INTENT, not the implementation. "Score leads in seconds, not half a minute", not "perf(scorer): cache keys". -->

## Read this first

- **For:** <the problem this solves, two plain lines a new reader can follow>
- **Changes:** <before -> after, with one concrete example>
- **Touches live systems:** <none | name each live system it writes to>
- **Evidence:** <the headline number, with its caveat in the same line>
- **Biggest risk:** <one line, and how to undo it>
- **Your decision:** <nothing, safe to integrate | the exact question Ben must answer>

---

## 1. Purpose and context
<What the system does here today, what was wrong or missing, and what this change is meant to achieve. Define each technical term the first time it appears.>

## 2. Behaviour change
- **Before:** 
- **After:** 
- **Example:** 

## 3. Where it sits
<Five lines at most: which component calls which, and what the output feeds. Not a tutorial.>

## 4. Results
<Small table. Baseline beside proposed. Sample size and the caveat next to every number. Say which results are measured on the evaluation data, which on held-out data, and which are only inferred from tests.>

## 5. Risks and what is unverified
<What could fail, what was not tested, and how to reverse the change.>

## 6. Code review guide
<The 2 to 5 files or functions that matter, in the order that helps a reviewer understand the change, with one line each on what it is responsible for.>

## 7. Verification
- `make check`: 
- CI: <link>
- <any live or manual check>
- **What these do not prove:** 

## 8. Patch size
<Lines of production code / tests / tooling / docs, and why that size is needed. Name any change outside the order's files and why.>

## 9. Learned
<Hard facts about the inputs, each with a source. Recorded as data at merge.>

## 10. Decided
<Lasting choices, with the option rejected. Promoted to DECISIONS.md at merge. Say "proposed, not decided" where Ben must rule.>
