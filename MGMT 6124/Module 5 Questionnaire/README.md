# MGMT-6124 Module 5: Questionnaire Assignment (Generative AI at Work and in School)

Work through the files in order.

| # | File | What it is |
|---|------|------------|
| 1 | `1_Questionnaire_Design_and_Fieldwork_Plan.docx` | Topic and rationale, hypotheses, the 14 questions, launch steps, outreach plan, roles, checklist |
| 2 | `2_Google_Form_Builder_create_form.gs` | Google Apps Script that builds the form (with branching) and its response sheet. Paste into script.google.com and run |
| 3 | `3_Survey_Analysis_Workbook.xlsx` | Empty analysis workbook. Paste the real export into `Responses!A1`; Summary, charts and cross-tabs fill themselves. Start on `Start_Here` |
| 4 | `4_Report_Template.docx` | The Word report, pre-structured to the grading criteria. Yellow = fill in, grey "Guide" lines = delete before submitting |

## Get your shareable survey link (about 3 minutes)

A link has to come from a form that lives in **your** Google account, so it cannot be generated for you. This script builds the whole form in one click.

1. Go to <https://script.google.com> and sign in with the Google account you want to own the survey. Use a personal Gmail account if your college account restricts sharing outside the school.
2. Click **New project**. Delete the starter code, paste in all of `2_Google_Form_Builder_create_form.gs`, and click **Save**.
3. In the toolbar choose the function **createSurvey** and click **Run**. Approve the permission prompts (it only touches the form and sheet it creates). If Google says the app is unverified, choose **Advanced > Go to project**. That is your own script.
4. Open **Execution log**. It prints three links:
   - `SHARE this link:` is the one you send to respondents.
   - `EDIT the form:` is where you can change wording (but see the note below).
   - `Response sheet:` is where answers arrive. Download it as `.xlsx` or `.csv` for the analysis workbook.
5. Test the share link in a private/incognito window: pick **Never** on Q3 (you should jump to the last page), then try again with **Daily**.
6. If the form says it is not published or not accepting responses, open it in edit mode and click **Publish**.

Do not change the wording of answer options after people start responding. The workbook counts the exact text.

**No Google account?** Build the form by hand from the table in section 4 of the design plan, or use Microsoft Forms / another free survey tool. The workbook only needs the column order to match.

No survey data is included anywhere. All results must come from your real respondents.
