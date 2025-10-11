// ***********************************************
// Custom Cypress commands for LGBTQ+ Analysis Tool
// ***********************************************

// Command to fill survey with specific values
Cypress.Commands.add('fillSurvey', (answers) => {
  Object.entries(answers).forEach(([key, value]) => {
    cy.get(`input[name="${key}"][value="${value}"]`).check()
  })
})

// Command to submit survey and wait for results
Cypress.Commands.add('submitSurvey', () => {
  cy.contains('คำนวณผลลัพธ์').click()
  cy.contains('ผลการวิเคราะห์', { timeout: 10000 }).should('be.visible')
})

// Command to switch language
Cypress.Commands.add('switchLanguage', (lang) => {
  const buttonText = lang === 'en' ? 'EN' : 'TH'
  cy.contains(buttonText).click()
})

// Command to check API health
Cypress.Commands.add('checkApiHealth', () => {
  cy.request(`${Cypress.env('apiUrl')}/health`).then((response) => {
    expect(response.status).to.eq(200)
  })
})
