# MGMT-6124 Module 5: Questionnaire Assignment (Generative AI at Work and in School)

**Team:** Adekunle Adeniji and Alain Rivera Sanchez

## The survey link (live)

**https://www.surveymonkey.com/r/PL9R5WL** (SurveyMonkey survey ID `423822152`, 14 questions, 3 pages, no responses yet when this was written).

Before you send it to anyone:

1. **Check your SurveyMonkey plan.** Free (Basic) plans have historically limited questions per survey and how many responses you can view or export, and the connector used to build this survey can only read the first 25 responses on a Basic plan. You need 30 or more. If the plan will not show you that many, use the Google Forms backup below.
2. **Test with Preview, not the live link.** Every submitted response (tests included) counts and has to be deleted before analysis.
3. **Turn on "Anonymous Responses"** in the collector settings if you want no IP addresses stored.
4. Fix any wording **before** launch. Changing options after responses arrive breaks the match with the analysis workbook.

What is different from the Google Forms version: SurveyMonkey has no skip logic through the connector, so Q4 to Q7 are on their own page marked "If you answered Never to Q3, skip this page" and are optional. Q10 says "Select up to 3" but is not capped.

When collection ends, export from SurveyMonkey (Analyze Results > Save As > Export All > All Responses Data > Excel) and give the file to Claude. It converts it to the workbook's layout and cross-checks counts against SurveyMonkey's own summary.

Work through the files in order.

| # | File | What it is |
|---|------|------------|
| 1 | `1_Questionnaire_Design_and_Fieldwork_Plan.docx` | Topic and rationale, hypotheses, the 14 questions, launch steps, outreach plan, roles, checklist |
| 2 | `2_Google_Form_Builder_create_form.gs` | Google Apps Script that builds the form (with branching) and its response sheet. Paste into script.google.com and run |
| 3 | `3_Survey_Analysis_Workbook.xlsx` | Empty analysis workbook. Paste the real export into `Responses!A1`; Summary, charts and cross-tabs fill themselves. Start on `Start_Here` |
| 4 | `4_Report_Template.docx` | The Word report, pre-structured to the grading criteria. Yellow = fill in, grey "Guide" lines = delete before submitting |

## Google Forms backup (about 3 minutes)

Use this if SurveyMonkey's plan limits get in the way. A Google Forms link has to come from a form that lives in **your** Google account, so it cannot be generated for you. This script builds the whole form in one click, with true skip logic.

1. Go to <https://script.google.com> and sign in with the Google account you want to own the survey. Use a personal Gmail account if your college account restricts sharing outside the school.
2. Click **New project**. Delete the starter code, paste in all of `2_Google_Form_Builder_create_form.gs`, and click **Save**.
3. In the toolbar choose the function **createSurvey** and click **Run**. Approve the permission prompts (it only touches the form and sheet it creates). If Google says the app is unverified, choose **Advanced > Go to project**. That is your own script.
4. Open **Execution log**. It prints three links:
   - `SHARE this link:` is the one you send to respondents.
   - `EDIT the form:` is where you can change wording (but see the note below).
   - `Response sheet:` is where answers arrive. Download it as `.xlsx` (whole file) or `.csv` (make sure the **Form Responses 1** tab is the active one, not the empty Sheet1) for the analysis workbook.
5. Test the share link in a private/incognito window while signed out of Google. It must open **without** asking you to sign in. If it does ask, open the form's **Settings** and set responders to **Anyone with the link** (turn off "Restrict to users in ..."), then test again. A school/Workspace account often defaults to restricted, which would block friends and family; a personal Gmail account does not.
6. Still in the private window, pick **Never** on Q3 (you should jump to the last page), then try again with **Daily**.
7. If the form says it is not published or not accepting responses, open it in edit mode and click **Publish**.

Do not change the wording of answer options after people start responding. The workbook counts the exact text.

**No Google account?** Build the form by hand from the table in section 4 of the design plan, or use Microsoft Forms / another free survey tool. The workbook only needs the column order to match.

No survey data is included anywhere. All results must come from your real respondents.
