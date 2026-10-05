# PRISM Request Design System

**Team Dart | MDPM 883 Assignment 3 | Prototype build rules**
**Status:** working draft for team review, 5 October 2026

This file governs how every PRISM Request screen is built. It exists so that every design component in the prototype comes from the Government of Alberta (GoA) Design System and nothing is invented. If a rule here conflicts with what the GoA components or the repository say, the repository wins and this file is wrong.

---

## 1. Authority and sources

| Source | What it governs | Version used |
|---|---|---|
| [GovAlta/ui-components](https://github.com/GovAlta/ui-components) | Components, props, events, wrapper pattern, standards | commit `67c5db6` (shallow clone, 5 Oct 2026) |
| `@abgov/design-tokens` | Colour, spacing, type, border and shadow tokens | `2.12.8` (the version pinned by the repository) |
| [design.alberta.ca](https://design.alberta.ca) | Published guidance, patterns, setup | Not read in this pass; the repository's own `docs/src/content` was read instead |
| PRISM Request Prototype Update Brief | What PRISM screens must do | Team Dart direction as of 3 October 2026 |

**Precedence when sources disagree:** (1) GoA repository and tokens, (2) this file, (3) the Prototype Update Brief on visual treatment only. The Brief still wins on product behaviour, scope and wording of the scenario.

**What this file does not do:** it does not copy component documentation. For any component, confirm props against `libs/react-components/src/lib/<component>/<component>.tsx` before use. Never rely on this file's prop lists alone.

---

## 2. Non-negotiable rules

These come from the repository's `CLAUDE.md`, `foundations/principles.mdx` and `foundations/anti-patterns.mdx`.

1. **Component first.** Search the GoA components before building anything. Ask the team before building a custom component.
2. **Props over CSS.** The components use shadow DOM. Do not target GoA classes, add `!important`, or wrap components in inline styles to restyle them.
3. **Tokens, never raw values.** No hex colours, pixel sizes or font sizes in PRISM code. Use `--goa-*` tokens. Where no token exists use `rem`.
4. **Spacing through component props.** Use `mt`, `mr`, `mb`, `ml` first, then `GoabBlock` for flex layouts, then `GoabGrid`. Use `GoabSpacer` only for an explicit gap.
5. **WCAG 2.2 AA is mandatory.** Use components that carry accessibility built in. Every icon-only control needs an accessible name.
6. **Do not claim a custom component is a GoA component.** Anything built outside `@abgov/react-components` is labelled "custom, prototype only" in reviewer notes (Brief section 3).
7. **No raw HTML for UI.** No `<button>`, `<input>`, `<a>`, `<select>`, `<textarea>` or heading tags where a `Goab*` component exists.

---

## 3. Setup (React)

React 17, 18 and 19 are supported. From the repository README:

```bash
npm i @abgov/react-components @abgov/web-components @abgov/ui-components-common
```

```ts
// src/main.tsx
import "@abgov/web-components";
```

```css
/* main stylesheet: includes the design tokens and dark theme overrides */
@import "@abgov/web-components/index.css";
```

Add the Ionicons script to `index.html` `<head>` exactly as the README gives it (version `8.1.0`, with its `integrity` hash). Wrap the app in `GoabThemeProvider`. `@abgov/styles` is deprecated; do not use it.

Naming: React components are `Goab*` (for example `GoabButton`), the underlying web components are `goa-*`. Event handlers are `onX` props and receive a detail object.

---

## 4. Which kind of product PRISM is

The design system distinguishes **citizen** products (guided, one question at a time, `AppHeader` + `AppFooter`) from **worker** products (dense, `WorkSideMenu`, no standard header or footer). Mixing them is rated a **Critical** anti-pattern.

**Decision for PRISM:** worker product (`workspace`). A CMAC is an internal Government of Alberta requester who returns to manage a list of work orders. Use `GoabWorkspaceLayout` with `GoabWorkSideMenu`. Do not add `GoabAppHeader` or `GoabAppFooter`.

**Caveat, from the content-design skill:** frequency can outrank role. Elena (two or three requests a year) is an occasional user, so her copy is written plain and calm, with guidance at the field. Priya (twenty-plus requests a year) wants dense, scannable lists. Layout follows the worker pattern; wording follows the reader.

The Brief's four-step creation flow is a guided sequence inside a worker product. That is allowed; keep each step to one purpose and do not turn the Dashboard into a one-question-per-page layout.

---

## 5. Tokens

Source: `@abgov/design-tokens` 2.12.8, `dist/tokens.css`. Use the variable name, never the value. Values are shown so reviewers can check contrast and consistency.

### 5.1 Colour

| Role | Token | Value |
|---|---|---|
| Body text | `--goa-color-text-default` | `#000000` |
| Secondary text | `--goa-color-text-secondary` | `#6f6f6f` (greyscale-600) |
| Text on dark | `--goa-color-text-light` | `#ffffff` |
| Disabled text | `--goa-color-text-disabled` | `#4d4d4d` (greyscale-700) |
| Link and primary action | `--goa-color-interactive-default` | `#006dcc` |
| Hover | `--goa-color-interactive-hover` | `#045092` |
| Visited link | `--goa-color-interactive-visited` | `#756693` |
| Focus ring | `--goa-color-interactive-focus` | `#006dcc` |
| Field error | `--goa-color-interactive-error` | `#ec040b` |
| Brand | `--goa-color-brand-default` / `-dark` / `-light` | `#0081a2` / `#005072` / `#c8eefa` |
| Information | `--goa-color-info-default` | `#0077ad` |
| Success | `--goa-color-success-default` | `#006f4c` |
| Warning / important | `--goa-color-warning-default` | `#f9ce2d` |
| Emergency | `--goa-color-emergency-default` | `#da291c` |
| Page and surface greys | `--goa-color-greyscale-white`, `-50`, `-100`, `-150`, `-200` | `#ffffff`, `#f8f8f8`, `#f2f0f0`, `#e9e9e9`, `#cdcdcd` |
| Borders and muted greys | `--goa-color-greyscale-300` to `-800` | `#b1b1b1`, `#9f9f9f`, `#808080`, `#6f6f6f`, `#4d4d4d`, `#353535` |

Each semantic family (`info`, `success`, `warning`, `emergency`, `important`) also has `-light`, `-dark`, `-text`, `-text-dark`, `-border` and `-background` variants. The extended palette (`sky`, `prairie`, `lilac`, `pasture`, `sunset`, `dawn`) exists for badges only.

**Colour never carries meaning alone.** Pair every semantic colour with text, and an icon where the component supports one (Brief section 3; QA item 3.3).

### 5.2 Spacing

| Token | `--goa-space-…` | Value |
|---|---|---|
| none | `none` | 0 |
| 3xs / 2xs / xs | `3xs`, `2xs`, `xs` | 0.125 / 0.25 / 0.5 rem |
| s / m / l | `s`, `m`, `l` | 0.75 / 1 / 1.5 rem |
| xl / 2xl / 3xl / 4xl | `xl`, `2xl`, `3xl`, `4xl` | 2 / 3 / 4 / 8 rem |

Component margin props accept the t-shirt names (`2xs` … `4xl`).

### 5.3 Typography

One font family: `--goa-font-family-sans` (`acumin-variable, helvetica-neue, arial, sans-serif`). Numbers may use `--goa-font-family-number` (`roboto-mono, monospace`) where a component applies it.

| Use | `GoabText` `size` | Weight | Size / line height |
|---|---|---|---|
| Page title | `heading-xl` (default for `h1`) | bold | 2.5 / 3 rem |
| Section heading | `heading-l` (default for `h2`) | bold | 2 / 2.5 rem |
| Subsection | `heading-m` | bold | 1.75 / 2.25 rem |
| Card or panel heading | `heading-s` | semi-bold | 1.5 / 1.75 rem |
| Group label | `heading-xs` | semi-bold | 1.25 / 1.5 rem |
| Minor label | `heading-2xs` | semi-bold | 1 / 1.375 rem |
| Large body | `body-l` | regular | 1.5 / 2.25 rem |
| Body | `body-m` | regular | 1.125 / 1.5 rem |
| Small body | `body-s` | regular | 1 / 1.375 rem |
| Caption, metadata | `body-xs` | regular | 0.875 / 1.25 rem |

`GoabText` takes `as` (`h1`–`h5`, `p`, `span`, `div`), `size`, `color` (`primary`, `secondary`, `light`, `disabled`), `maxWidth` (default `65ch`) and the margin props. Keep one `h1` per page and do not skip heading levels.

### 5.4 Shape and elevation

Borders: `--goa-border-width-s` (1px) default; `-l` (2px) for emphasis. Radii: `--goa-border-radius-m` (0.5rem) is the common default; `-xs`, `-s`, `-l` exist. Shadows: only `--goa-shadow-modal`, `--goa-shadow-raised-light` and `--goa-shadow-shallow-below`, and only where a component already applies them. The Brief asks for minimal shadows; do not add any.

### 5.5 Responsive

Breakpoints from the repository: mobile 624px, tablet 1024px. The Brief fixes the prototype at a 1440px desktop view; layouts must still reflow without horizontal scrolling.

---

## 6. Component map for PRISM

Component names are the React exports in `@abgov/react-components`. Enum values below were read from `libs/common/src/lib/common.ts`.

### 6.1 Shell and layout

| PRISM element | Component | Notes |
|---|---|---|
| Whole app frame | `GoabWorkspaceLayout` | Host it directly at the router outlet, not inside another scrolling container (`workspace-layout-host-at-viewport-root`). Slots: `sideMenu`, `pageHeader`, `pageFooter`, `pushDrawer`. |
| Primary navigation: Dashboard, My Requests, Help | `GoabWorkSideMenu` + `GoabWorkSideMenuItem` (`label`, `url`, `icon`, `badge`, `current`) | Three items only (Brief section 4). Use `badge` for an unread count, not a custom dot. |
| Profile, Settings, Sign Out | `GoabWorkSideMenu` `accountContent` / `userName` / `userSecondaryText` | Brief calls this the avatar menu. Confirm the slot renders the three actions before building a custom menu; if it cannot, use `GoabMenuButton` with `GoabMenuAction` and record it as a deviation. |
| Page width and rhythm | `GoabBlock`, `GoabGrid` (`minChildWidth`, `gap`), `GoabSpacer`, `GoabDivider` | `GoabContainer` is not for layout (`container-not-for-layout`). |

### 6.2 Forms

Every form control sits inside a `GoabFormItem` (`form-inputs-require-formitem`).

| PRISM element | Component | Key props |
|---|---|---|
| Field wrapper | `GoabFormItem` | `label`, `labelSize` (`compact`, `regular`, `large`), `requirement` (`optional`, `required`), `helpText`, `error` |
| Text, email, telephone, number | `GoabInput` | `type` (`text`, `email`, `tel`, `number`, `date` …), `name`, `value`, `error`, `onChange` |
| Description | `GoabTextArea` | `rows`, `countBy`, `maxCount`, `error` |
| Searchable select (Ministry, Facility, Manufacturer) | `GoabDropdown` + `GoabDropdownItem` | `filterable`, `noResults`, `placeholder`, `native` |
| Short fixed lists (Priority, Funding, Request Reason) | `GoabDropdown` | Same component without `filterable` |
| Service category and request-type choice (radio cards) | `GoabRadioGroup` + `GoabRadioItem` | `description` gives the short explanation under each option; `reveal` shows the Furniture request-type selector after Furniture is chosen |
| Date Required | `GoabDatePicker` | `type` input variant for keyboard entry, `min`, `max` |
| Quantity | `GoabInput` `type="number"` | Whole numbers only; enforce in validation, not by CSS |
| Draft versus submit actions | `GoabButtonGroup` with `GoabButton` | See 6.3 |
| Step indicator | `GoabFormStepper` + `GoabFormStep` | `step` sets the current step. In the web component, `step` of `-1` makes navigation free and any other value makes it constrained; see section 8 for the open choice |
| Optional explanation inline | `GoabDetails` | Not stacked (`details-dont-stack`); fine inside forms |

### 6.3 Buttons and links

| PRISM action | Component and props |
|---|---|
| Create Work Order, Continue, Submit request | `GoabButton` `type="primary"` (`submit` inside a real form). **One primary per page.** |
| Back, Save draft, Edit | `GoabButton` `type="secondary"` or `tertiary` |
| Compact table or row actions | `GoabButton` `size="compact"`, or `GoabIconButton` with an accessible name |
| Destructive: Remove file, Leave without saving | `GoabButton` `variant="destructive"`, only on the final confirming action, with descriptive wording |
| Navigate to another page | `GoabLink`. Use a link to navigate and a button to act (`button-vs-link`). |
| Prominent navigation to a start page | `GoabLinkButton` |

Button labels are sentence case and concise: "Create work order", not "CREATE WORK ORDER". The Brief's capitalised names (Create Work Order, My Requests) are product names in navigation; use sentence case on buttons unless the team decides otherwise.

### 6.4 Status, feedback and messaging

| PRISM element | Component | Rule |
|---|---|---|
| Lifecycle stage (Submitted, Reviewing, Fulfilling, Closed) | `GoabBadge` | `type` ∈ `information`, `success`, `important`, `emergency`, `archived`, `default`, plus extended colours. Always include the stage text in `content`; sentence case, short. Do not style a badge like a button and do not use interactive colours for it. |
| Attention flag (Information required, Action required, Waiting on client, No action required) | `GoabBadge` with `icon` / `iconType` | Kept separate from the stage badge (Brief section 14). Pair colour with the icon and the text. |
| Unread marker | `GoabBadge` or a menu `badge` count | Separate from stage and from "action required". |
| Page-level notice (information request pending, prototype notice) | `GoabNotification` | `type` ∈ `important`, `information`, `event`, `emergency`; one at a time; concise. |
| Inline explanation, "this is a prototype" statement, proposal status | `GoabCallout` | `type` ∈ `information`, `success`, `important`, `emergency`, `event`. **Never for form validation** (`callout-not-for-validation`). Not dismissible. |
| Form validation | `GoabFormItem` `error` plus an error summary linking to fields | Field-level messages state the fix with an example, not what went wrong. |
| "Draft saved at …", "Message sent" | `GoabTemporaryNotificationCtrl` | Never for errors (`temporary-notification-not-for-errors`). |
| Loading | `GoabSkeleton` (content shape), `GoabCircularProgress`, `GoabLinearProgress`, `GoabSpinner` | Skeleton should match the content shape. |

### 6.5 Lists, tabs, panels and overlays

| PRISM element | Component | Rule |
|---|---|---|
| My Requests list | `GoabTable` + `GoabTableSortHeader` | `variant="relaxed"` for long text; semantic structure; sortable columns. Add `GoabPagination` only when needed. |
| List filters (All, Drafts, Needs my attention, In progress, Closed) | `GoabFilterChip` or a `GoabTabs` segmented control | Filters are list views, not lifecycle stages (Brief section 6). |
| Search | `GoabInput` `type="search"` with a `leadingIcon` | Wrapped in `GoabFormItem` or given `ariaLabel`. |
| Request tabs: Overview, Activity & Messages, Attachments, Proposal & Costs | `GoabTabs` + `GoabTab` | Short labels, one preselected tab. Do not nest tabs, do not use tabs to show progress, and do not use tabs when the user needs two tabs visible at once. |
| Checklist helper, wide screens | `GoabPushDrawer` | Reference-task pattern; it pushes content instead of covering it (`push-drawer-use-for-reference-tasks`). |
| Checklist helper, narrow screens | `GoabDrawer` (`position` right or bottom) | Push drawers fall back on mobile. |
| Confirm leave without saving | `GoabModal` | `role="alertdialog"` for critical choices; actions are Save and leave, Leave without saving, Stay. Do not give both actions and a close icon (`modal-dont-actions-and-close`). |
| Upload area | `GoabFileUploadInput` (`variant` `dragdrop` or `button`, `accept`, `maxFileSize`) | Show the maximum size and accepted types as helper text. |
| Uploaded file row | `GoabFileUploadCard` (`filename`, `size`, `type`, `progress`, `error`, `onDelete`, `onCancel`) | Pair the input and the cards (`fileupload-pair-input-card`). Progress and error states come from these props. |
| Collapsible help | `GoabDetails` or `GoabAccordion` | Do not hide critical content. |

### 6.6 Components not to build

Do not hand-build: buttons, form fields, tabs, badges, modals, drawers, notifications, tables, steppers, the side menu, or file upload. If a PRISM need has no GoA component (for example a message thread or a lifecycle timeline), build it from `GoabBlock`, `GoabText`, `GoabBadge`, `GoabDivider` and tokens, name it in reviewer notes as **custom, prototype only**, and ask the team before extending it.

---

## 7. Screen patterns

Each pattern states the components to compose. Details of behaviour stay in the Prototype Update Brief.

| Screen | Composition |
|---|---|
| **Dashboard** | `GoabText` h1 "Welcome, Kevin." · primary `GoabButton` Create work order · "Needs your attention" and "Drafts to resume" as compact `GoabTable`s or short lists · `GoabLink` View all requests. No repeated full request details across cards. |
| **My Requests** | Search `GoabInput` · filter chips · `GoabTable` with columns Work order number or Draft, Title, Location, Stage, Current owner, Next action, Last updated · empty state with a next action. |
| **Create: four steps** | `GoabFormStepper` (4 steps: Request Type, Request Details, Attachments, Review & Submit) · `GoabFormItem`-wrapped controls · `GoabButtonGroup` with Back, Save draft, Continue. One primary button per page. |
| **Request Type** | `GoabRadioGroup` of service categories with `description` · `reveal` the furniture request-type `GoabRadioGroup` · helper in a `GoabPushDrawer`. |
| **Request Details** | Sections as headed groups (`GoabText` h2) in a `GoabGrid` · `GoabDropdown` for ministry, facility, manufacturer, classification · `GoabDatePicker` for date required · error summary at top on failure. |
| **Attachments** | `GoabFileUploadInput` + one `GoabFileUploadCard` per file · each file's classification in a `GoabDropdown` · state shown as text, never colour alone. |
| **Review & Submit** | Per-section summary with an Edit `GoabLink` or secondary `GoabButton` · three groups of messages (blocking, needs confirmation, advisory) as `GoabCallout`s with correction links · Submit request stays **enabled** (see 8.1). |
| **Submission confirmation** | `GoabCallout` `type="success"` with heading "Request submitted" · facts in a `GoabBlock` list: work order number, title, location, submitted time, Stage `GoabBadge` "Submitted", Detailed status "Awaiting initial review", Review queue, Furniture Coordinator "Not yet assigned" · View request and Back to My Requests. |
| **Request overview** | Header with title and stage `GoabBadge` · attention `GoabBadge` · `GoabTabs` · overview facts: stage, detailed status, responsible person or team, pending item, next action, last updated. |
| **Proposal & Costs** | `GoabTable` of source, quantity, furniture cost, delivery cost, expected timing, with a total · client decision shown as `GoabBadge` "Pending" · "Record client decision" in a `GoabModal` or `GoabDrawer`. |
| **Messages** | Custom thread (see 6.6) with author, role, time, attachments · composer: `GoabTextArea` + `GoabFileUploadInput` + Save draft + Send message · "Draft — not sent" as a visible `GoabBadge`. |
| **Help, Profile** | `GoabAccordion` or headed sections of `GoabText`; profile fields in read-only `GoabFormItem`s with a note about what is profile-managed. |

---

## 8. Conflicts between the Brief and the GoA guidance

These must be decided by the team. Until they are, build as marked.

| # | Brief or QA position | GoA guidance | Build as |
|---|---|---|---|
| 8.1 | QA 1.9 recommends "Submit inactive" while gaps exist. | `button-avoid-disabled` and `button-enabled-with-error-handling` say keep buttons enabled and explain errors on submit. The repository also ships a "disabled button with a required field" example, so the guidance is not absolute. | Keep **Submit request enabled**; on press show the error summary with links. This matches the Brief's "error summary linking to affected fields". Update QA 1.9. |
| 8.2 | Brief: neutral wireframe, no production-brand styling. | GoA components carry GoA styling and cannot be restyled without breaking the system. | Use GoA components and tokens unmodified. Neutral comes from restraint (no illustrations, no extra shadows, no decorative colour), not from overriding styles. |
| 8.3 | Brief: place Joy's message beside the proposal, and keep a two-sided history in Activity & Messages. | `tabs-dont-need-multiple-visible`: do not put content in separate tabs if users must see it together. | Show Joy's latest message on the Proposal & Costs tab and link to the full thread in Activity & Messages. |
| 8.4 | Brief: completed steps can be revisited; stepper behaviour not specified. | `GoabFormStepper` is free (`step` of `-1`) or constrained (any other `step`); `dont-use-stepper-for-nonsequential`. | Four sequential steps: acceptable. Use free navigation only if jumping forward over incomplete steps is acceptable; otherwise constrained. Record the choice. |
| 8.5 | Brief: avatar menu with My Profile, Settings, Sign Out. | `GoabWorkSideMenu` provides an account area. | Verify it supports three actions; otherwise record a deviation. |
| 8.6 | Brief: capitalised button and menu names. | `button-sentence-case`. | Sentence case on buttons and labels. |
| 8.7 | Brief: radio cards. | `GoabRadioItem` supports `description` and `reveal`; it is not a card. | Use radio items with descriptions. Do not build card-style radios. |

---

## 9. Content rules

From `skills/content-design/SKILL.md` and the GoA writing guidance.

1. **Name the reader first.** Occasional requester: plain language, one idea at a time, calm. Frequent requester: dense, scannable, action first.
2. **Verbs, not program names.** "Report a problem with the delivery", not "Issue Report module". Expand acronyms unless the reader knows the acronym better. Keep `[PM]` as the legacy routing label and do not expand it (Brief section 8).
3. **Errors state the fix** with an example of valid input. Do not repeat "error" in words when the field is already styled as an error.
4. **Empty states give the next action.**
5. **Notifications front-load the point** because they truncate.
6. **No unverified claims.** Words like "approved", "confirmed", "official" appear only where the Brief permits. A work order number confirms receipt, not approval.
7. **No em or en dashes.** Use full stops or commas. Sentence case for labels, buttons, tabs and badges.
8. **Prototype data is labelled.** Placeholders such as "Not supplied" stay visible; never replace them with invented figures.
9. **Roles, not private details.** Use sample data only.

---

## 10. Accessibility checklist

- Every control has a label (`GoabFormItem` label or `ariaLabel`). Icon-only buttons and badges have an accessible name.
- Colour is never the only carrier of status; stage, attention and file states are always text too.
- Visible focus on every control (the components provide it; do not remove it).
- One `h1`; headings in order; page order matches visual order.
- Error summary links move focus to the field.
- Dialogs and drawers return focus to the control that opened them.
- Works at 200 per cent zoom and by keyboard only (Revision 2, section 6.2).
- Table headers are semantic (`table-semantic-structure`).

---

## 11. Review checklist (use before every pull request)

- [ ] Every UI element is a `Goab*` component or listed as custom in reviewer notes.
- [ ] No raw interactive HTML or heading elements.
- [ ] No hex colours, pixel values or font sizes; only `--goa-*` tokens or `rem`.
- [ ] Spacing through component margin props, `GoabBlock` or `GoabGrid`.
- [ ] One primary button per page; sentence-case labels.
- [ ] Every form control inside `GoabFormItem`.
- [ ] Validation uses `error` and an error summary, not a callout.
- [ ] Stage, attention and unread are three separate things on screen.
- [ ] Prototype hypotheses and unknowns named in reviewer notes.
- [ ] Enum values and props checked against the component source, not this file.

---

## 12. Open items for the team

1. Confirm worker-product decision (section 4).
2. Decide each item in section 8.
3. Confirm whether the account menu can carry three actions (8.5).
4. Confirm the version pins above are those used by the Make project (`package.json` was not available to this review).
5. Section 8.1 changes QA item 1.9; section 8.3 changes the placement in QA item 2.10.
