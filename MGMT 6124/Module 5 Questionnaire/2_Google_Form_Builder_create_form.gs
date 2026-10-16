/**
 * Builds the survey "Generative AI at Work and School: A Short Survey" in Google Forms,
 * plus a linked Google Sheet that collects the responses.
 *
 * HOW TO RUN (2 minutes)
 *  1. Go to https://script.google.com and click New project.
 *  2. Delete the starter code, paste this whole file, click Save.
 *  3. Choose the function "createSurvey" in the toolbar and click Run.
 *  4. Approve the permissions (Forms, Sheets, Drive: it only touches the form and sheet it creates).
 *  5. Open View > Logs (or Execution log). You get 3 links: the form to EDIT, the form to SHARE, and the response sheet.
 *  6. Open the form, click the Settings tab, and check "Responses > Collect email addresses" is OFF (anonymous survey).
 *
 * IMPORTANT: the option wording below is what the Excel workbook counts. If you reword an option here,
 * reword the matching label on the workbook's Summary / XTab sheets too (the 'Unmatched answers' check will tell you).
 *
 * Generated from the same question spec as the workbook and the design document.
 */
function createSurvey() {
  var form = FormApp.create("Generative AI at Work and School: A Short Survey");
  form.setDescription(
    "A 4-minute anonymous survey for a college business analysis course. " +
    "It asks how people use generative AI tools (like ChatGPT, Copilot, Gemini or Claude) at work and in school, " +
    "and what support they need. Taking part is voluntary, no names or emails are collected, " +
    "and results are only reported as group totals. You must be 18 or older. Thank you!");
  form.setCollectEmail(false);
  form.setProgressBar(true);
  form.setShowLinkToRespondAgain(false);
  form.setAllowResponseEdits(false);
  form.setConfirmationMessage("Thank you for taking part! Your response has been recorded.");

  // ---------- Page 1: About you (+ Q3, which branches) ----------
  form.addSectionHeaderItem().setTitle("About you").setHelpText("Two quick questions so we can compare groups.");

  form.addMultipleChoiceItem().setTitle("Q1. Which age group are you in?").setChoiceValues(["18 to 24", "25 to 34", "35 to 44", "45 or older"]).setRequired(true);
  form.addMultipleChoiceItem().setTitle("Q2. Which best describes what you do right now?").setChoiceValues(["Student only", "Employed only (full-time or part-time)", "Both student and employed", "Neither at the moment"]).setRequired(true);
  // Q3 uses page navigation, so its choices are set after the later pages exist.
  var q3 = form.addMultipleChoiceItem().setTitle("Q3. How often do you use generative AI tools (for example ChatGPT, Copilot, Gemini or Claude) for work or study?").setChoiceValues(["Never", "Less than once a month", "A few times a month", "A few times a week", "Daily"]).setHelpText("Choosing \"Never\" skips the next page of questions about using AI tools.").setRequired(true);

  // ---------- Page 2: users of AI tools only ----------
  var pageUsers = form.addPageBreakItem().setTitle("Your experience using AI tools").setHelpText("These questions are about how you use AI tools.");
  form.addCheckboxItem().setTitle("Q4. Which tasks do you use AI tools for? Select all that apply.").setChoiceValues(["Writing or editing", "Research or summarizing", "Brainstorming ideas", "Analyzing data or spreadsheets", "Coding or technical help", "Translation or language support", "Scheduling or admin tasks"]).setRequired(true);
  form.addMultipleChoiceItem().setTitle("Q5. On average, about how much time per week do AI tools save you?").setChoiceValues(["None - no time saved", "Less than 1 hour", "1 to 3 hours", "4 to 6 hours", "7 or more hours"]).setRequired(true);
  form.addGridItem().setTitle("Q6. How much do you agree with each statement about your own use of AI tools?").setRows(["AI tools help me complete tasks faster.", "AI tools improve the quality of my work.", "I always check AI-generated output before I use it."]).setColumns(["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"]).setRequired(true);
  form.addScaleItem().setTitle("Q7. How confident are you in your ability to use AI tools effectively?").setBounds(1, 5).setLabels("Not at all confident", "Very confident").setRequired(true);

  // ---------- Page 3: everyone ----------
  var pageAll = form.addPageBreakItem().setTitle("Your workplace or school, and the future").setHelpText("Last page. These questions are for everyone, whether or not you use AI tools.");
  form.addMultipleChoiceItem().setTitle("Q8. Which best describes the guidance you have received about using AI tools from your employer or school?").setChoiceValues(["Formal training", "Written policy or guidelines only", "Informal advice only", "No guidance at all"]).setRequired(true);
  form.addMultipleChoiceItem().setTitle("Q9. Which best describes your employer's or school's current approach to AI tools?").setChoiceValues(["Encouraged and supported", "Allowed with rules", "Discouraged or restricted", "Banned", "Not sure or no policy"]).setRequired(true);
  var q10 = form.addCheckboxItem().setTitle("Q10. What are the biggest barriers to using AI tools (more) in your work or study? Select up to 3.").setChoiceValues(["Concerns about accuracy", "Data privacy or confidentiality concerns", "Rules or policy restrictions", "Lack of training or skills", "Cost of tools", "Academic or professional integrity concerns", "I do not see a need"]).setRequired(true);
  q10.setValidation(FormApp.createCheckboxValidation()
      .setHelpText("Please select up to 3 options.")
      .requireSelectAtMost(3)
      .build());
  form.addScaleItem().setTitle("Q11. \"AI will reduce job opportunities in my field over the next 5 years.\" How much do you agree?").setBounds(1, 5).setLabels("Strongly disagree", "Strongly agree").setRequired(true);
  form.addMultipleChoiceItem().setTitle("Q12. If your employer or school invested in ONE of these, which would help you most?").setChoiceValues(["Approved and secure AI tools", "Training workshops", "Clear policy and guidelines", "Time to experiment with tools", "None of these - no investment needed"]).setRequired(true);
  form.addMultipleChoiceItem().setTitle("Q13. Over the next 12 months, do you expect your use of AI tools to change?").setChoiceValues(["Increase a lot", "Increase a little", "Stay about the same", "Decrease", "I do not expect to use AI tools"]).setRequired(true);
  form.addParagraphTextItem().setTitle("Q14. In a sentence or two, what is the single biggest benefit or risk of AI tools for your work or study? (optional)").setRequired(false);

  // ---------- Branching: "Never" on Q3 skips page 2 (Q4 to Q7) and jumps to page 3 ----------
  q3.setChoices([
    q3.createChoice("Never", pageAll),
    q3.createChoice("Less than once a month", FormApp.PageNavigationType.CONTINUE),
    q3.createChoice("A few times a month", FormApp.PageNavigationType.CONTINUE),
    q3.createChoice("A few times a week", FormApp.PageNavigationType.CONTINUE),
    q3.createChoice("Daily", FormApp.PageNavigationType.CONTINUE)
  ]);

  // ---------- Collect answers in a Google Sheet ----------
  var ss = SpreadsheetApp.create("Generative AI at Work and School: A Short Survey (Responses)");
  form.setDestination(FormApp.DestinationType.SPREADSHEET, ss.getId());

  Logger.log("EDIT the form:      " + form.getEditUrl());
  Logger.log("SHARE this link:    " + form.getPublishedUrl());
  Logger.log("Response sheet:     " + ss.getUrl());
  Logger.log("Reminder: the report needs a link to your survey results. Share the response sheet 'view only' and paste its link into the report.");
}
