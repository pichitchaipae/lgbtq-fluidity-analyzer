/**
 * E2E Tests for Version 2.0 Advanced Analysis Features
 * Tests: AI Mode, ANOVA Results, Charts, Bilingual Interpretation
 */

describe('Advanced Analysis v2.0', () => {
  beforeEach(() => {
    cy.visit('/')
    // Fill out survey with test data
    fillSurvey()
  })

  it('should display Advanced Analysis button after survey completion', () => {
    cy.get('[data-testid="advanced-analysis-button"]')
      .should('be.visible')
      .and('contain', 'Advanced Analysis')
  })

  it('should open mode selector dialog when clicking Advanced Analysis', () => {
    cy.get('[data-testid="advanced-analysis-button"]').click()
    
    // Check dialog appears
    cy.get('[data-testid="mode-selector-dialog"]')
      .should('be.visible')
    
    // Check both mode options are present
    cy.get('[data-testid="local-mode-button"]')
      .should('be.visible')
      .and('contain', 'Local Mode')
    
    cy.get('[data-testid="ai-mode-button"]')
      .should('be.visible')
      .and('contain', 'AI Mode')
  })

  describe('Local Mode Analysis', () => {
    beforeEach(() => {
      cy.get('[data-testid="advanced-analysis-button"]').click()
      cy.get('[data-testid="local-mode-button"]').click()
    })

    it('should display ANOVA results without AI interpretation', () => {
      // Wait for analysis to complete
      cy.get('[data-testid="anova-results"]', { timeout: 10000 })
        .should('be.visible')
      
      // Check statistical results are displayed
      cy.get('[data-testid="f-statistic"]').should('exist')
      cy.get('[data-testid="p-value"]').should('exist')
      cy.get('[data-testid="eta-squared"]').should('exist')
      
      // Verify no AI interpretation in local mode
      cy.get('[data-testid="ai-interpretation"]').should('not.exist')
    })

    it('should display charts for each dimension', () => {
      cy.get('[data-testid="anova-results"]', { timeout: 10000 })
        .should('be.visible')
      
      // Check for charts
      cy.get('[data-testid="chart-sexual-orientation"]').should('be.visible')
      cy.get('[data-testid="chart-gender-identity"]').should('be.visible')
      cy.get('[data-testid="chart-attraction-patterns"]').should('be.visible')
    })
  })

  describe('AI Mode Analysis', () => {
    beforeEach(() => {
      cy.get('[data-testid="advanced-analysis-button"]').click()
      cy.get('[data-testid="ai-mode-button"]').click()
    })

    it('should display loading state while AI is processing', () => {
      cy.get('[data-testid="ai-loading"]')
        .should('be.visible')
        .and('contain', 'AI is analyzing')
    })

    it('should display ANOVA results with AI interpretation', () => {
      // Wait for AI analysis (can take 2-10 seconds)
      cy.get('[data-testid="anova-results"]', { timeout: 15000 })
        .should('be.visible')
      
      // Check statistical results
      cy.get('[data-testid="f-statistic"]').should('exist')
      cy.get('[data-testid="p-value"]').should('exist')
      
      // Verify AI interpretation is present
      cy.get('[data-testid="ai-interpretation"]', { timeout: 15000 })
        .should('be.visible')
        .and('not.be.empty')
    })

    it('should display bilingual AI interpretation (Thai + English)', () => {
      cy.get('[data-testid="ai-interpretation"]', { timeout: 15000 })
        .should('be.visible')
      
      // Check for Thai content (contains Thai characters)
      cy.get('[data-testid="ai-interpretation-thai"]')
        .should('be.visible')
        .invoke('text')
        .should('match', /[\u0E00-\u0E7F]/) // Thai Unicode range
      
      // Check for English content
      cy.get('[data-testid="ai-interpretation-english"]')
        .should('be.visible')
        .invoke('text')
        .should('match', /[a-zA-Z]/)
    })

    it('should display privacy notice with AI provider name', () => {
      cy.get('[data-testid="privacy-notice"]', { timeout: 15000 })
        .should('be.visible')
        .and('contain', 'Privacy Notice')
        .and('match', /(Google Gemini|OpenAI)/) // Either provider
    })

    it('should display all charts with AI insights', () => {
      cy.get('[data-testid="anova-results"]', { timeout: 15000 })
        .should('be.visible')
      
      // Verify charts are rendered
      cy.get('[data-testid="chart-container"]').should('have.length.at.least', 3)
    })
  })

  describe('Error Handling', () => {
    it('should show error message if AI service fails', () => {
      // Intercept API call and force error
      cy.intercept('POST', '/api/v2/analysis', {
        statusCode: 500,
        body: { detail: 'AI service temporarily unavailable' }
      }).as('analysisError')
      
      cy.get('[data-testid="advanced-analysis-button"]').click()
      cy.get('[data-testid="ai-mode-button"]').click()
      
      cy.wait('@analysisError')
      
      cy.get('[data-testid="error-message"]')
        .should('be.visible')
        .and('contain', 'unavailable')
    })

    it('should fallback to local mode if AI fails', () => {
      // Intercept and force AI error but return local results
      cy.intercept('POST', '/api/v2/analysis', {
        statusCode: 200,
        body: {
          anova_results: getMockAnovaResults(),
          ai_interpretation: null,
          error: 'AI service unavailable, showing local results'
        }
      })
      
      cy.get('[data-testid="advanced-analysis-button"]').click()
      cy.get('[data-testid="ai-mode-button"]').click()
      
      // Should show results without AI interpretation
      cy.get('[data-testid="anova-results"]').should('be.visible')
      cy.get('[data-testid="ai-interpretation"]').should('not.exist')
      cy.get('[data-testid="fallback-notice"]')
        .should('be.visible')
        .and('contain', 'local results')
    })
  })

  describe('Accessibility', () => {
    it('should be keyboard navigable', () => {
      cy.get('[data-testid="advanced-analysis-button"]').focus()
      cy.focused().type('{enter}')
      
      cy.get('[data-testid="mode-selector-dialog"]').should('be.visible')
      
      cy.get('[data-testid="local-mode-button"]').focus()
      cy.focused().should('have.attr', 'data-testid', 'local-mode-button')
    })

    it('should have proper ARIA labels', () => {
      cy.get('[data-testid="advanced-analysis-button"]')
        .should('have.attr', 'aria-label')
      
      cy.get('[data-testid="advanced-analysis-button"]').click()
      
      cy.get('[data-testid="mode-selector-dialog"]')
        .should('have.attr', 'role', 'dialog')
        .and('have.attr', 'aria-labelledby')
    })
  })
})

/**
 * Helper function to fill survey with test data
 */
function fillSurvey() {
  // Sexual Orientation questions (assuming 5 questions per dimension)
  const responses = [
    { question: 1, value: 3 },
    { question: 2, value: 4 },
    { question: 3, value: 2 },
    { question: 4, value: 5 },
    { question: 5, value: 3 },
    { question: 6, value: 4 },
    { question: 7, value: 3 },
    { question: 8, value: 4 },
    { question: 9, value: 2 },
    { question: 10, value: 5 }
  ]

  responses.forEach(({ question, value }) => {
    cy.get(`[data-testid="question-${question}"]`)
      .find(`[data-value="${value}"]`)
      .click()
  })

  // Submit survey
  cy.get('[data-testid="submit-survey"]').click()
}

/**
 * Mock ANOVA results for testing
 */
function getMockAnovaResults() {
  return {
    sexual_orientation: {
      F: 12.45,
      p: 0.001,
      eta_squared: 0.34,
      df_between: 2,
      df_within: 97,
      significant: true
    },
    gender_identity: {
      F: 8.32,
      p: 0.015,
      eta_squared: 0.21,
      df_between: 3,
      df_within: 96,
      significant: true
    },
    attraction_patterns: {
      F: 15.78,
      p: 0.0001,
      eta_squared: 0.42,
      df_between: 4,
      df_within: 95,
      significant: true
    }
  }
}
