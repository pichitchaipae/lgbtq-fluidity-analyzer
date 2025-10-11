describe('LGBTQ+ Sexual Fluidity Analysis Tool - E2E Tests', () => {
  beforeEach(() => {
    cy.visit('/')
  })

  describe('Homepage and Language Toggle', () => {
    it('should load the homepage successfully', () => {
      cy.contains('LGBTQ+').should('be.visible')
      cy.contains('🏳️‍🌈').should('be.visible')
    })

    it('should display privacy badges', () => {
      cy.contains('ไม่เก็บข้อมูล').should('be.visible')
      cy.contains('เชิงสถิติ').should('be.visible')
      cy.contains('SDG').should('be.visible')
    })

    it('should toggle between Thai and English', () => {
      // Default is Thai
      cy.contains('เครื่องมือวิเคราะห์').should('be.visible')
      
      // Click language toggle
      cy.contains('EN').click()
      
      // Should show English
      cy.contains('Analysis Tool').should('be.visible')
      cy.contains('No Data Collection').should('be.visible')
      
      // Toggle back to Thai
      cy.contains('TH').click()
      cy.contains('เครื่องมือวิเคราะห์').should('be.visible')
    })
  })

  describe('Survey Form', () => {
    it('should display all question groups', () => {
      cy.contains('การเปิดรับสื่อ').should('be.visible')
      cy.contains('ครอบครัวและเพื่อน').should('be.visible')
      cy.contains('ชุมชนออนไลน์').should('be.visible')
      cy.contains('วัฒนธรรมและภาษา').should('be.visible')
      cy.contains('การสำรวจตัวตน').should('be.visible')
      cy.contains('สภาพแวดล้อมทางการศึกษา').should('be.visible')
    })

    it('should allow selecting answers', () => {
      // Select first dropdown and change value
      cy.get('select').first().select('1')
      cy.get('select').first().should('have.value', '1')
    })

    it('should show submit and reset buttons', () => {
      cy.contains('คำนวณผลลัพธ์').should('be.visible')
      cy.contains('ล้างข้อมูล').should('be.visible')
    })
  })

  describe('Survey Submission and Results', () => {
    it('should submit survey and show results', () => {
      // Fill out all select dropdowns with value 0
      cy.get('select').each(($select) => {
        cy.wrap($select).select('0')
      })

      // Submit form
      cy.contains('คำนวณผลลัพธ์').click()

      // Wait for success message
      cy.contains('ประมวลผลสำเร็จ', { timeout: 15000 }).should('be.visible')
      
      // Check for score display
      cy.contains('%', { timeout: 5000 }).should('be.visible')
      
      // Check for emoji interpretation
      cy.get('p').contains(/🌙|🌱|🦋|🏳️‍🌈/, { timeout: 5000 }).should('exist')
    })

    it('should display all section scores', () => {
      // Fill and submit
      cy.get('select').each(($select) => {
        cy.wrap($select).select('0')
      })

      cy.contains('คำนวณผลลัพธ์').click()

      // Wait for success
      cy.contains('ประมวลผลสำเร็จ', { timeout: 15000 }).should('be.visible')

      // Check for section labels with emojis (scroll to make sure they're visible)
      cy.contains('📺', { timeout: 5000 }).scrollIntoView().should('be.visible')  // Media
      cy.contains('👨‍👩‍👧‍👦', { timeout: 5000 }).scrollIntoView().should('be.visible')  // Family (4 people)
      cy.contains('🌐', { timeout: 5000 }).scrollIntoView().should('be.visible')  // Online (globe)
      cy.contains('💬', { timeout: 5000 }).scrollIntoView().should('be.visible')  // Culture (speech)
      cy.contains('🔍', { timeout: 5000 }).scrollIntoView().should('be.visible')  // Exploration
      cy.contains('🏫', { timeout: 5000 }).scrollIntoView().should('be.visible')  // School
    })

    it('should show disclaimer and references', () => {
      cy.get('select').each(($select) => {
        cy.wrap($select).select('0')
      })
      cy.contains('คำนวณผลลัพธ์').click()

      // Wait for success
      cy.contains('ประมวลผลสำเร็จ', { timeout: 15000 }).should('be.visible')

      // Scroll to disclaimer section
      cy.contains('หมายเหตุ', { timeout: 5000 }).scrollIntoView().should('be.visible')
      cy.contains('เอกสารอ้างอิง', { timeout: 5000 }).scrollIntoView().should('be.visible')
      cy.contains('Diamond', { timeout: 5000 }).scrollIntoView().should('be.visible')  // Reference author
    })
  })

  describe('Results with English Language', () => {
    it('should show results in English after language toggle', () => {
      // Switch to English
      cy.contains('EN').click()

      // Fill survey
      cy.get('select').each(($select) => {
        cy.wrap($select).select('0')
      })

      // Submit
      cy.contains('Calculate Results').click()

      // Wait for success message
      cy.contains('Processing successful', { timeout: 15000 }).should('be.visible')

      // Check English results (scroll to make visible)
      cy.contains('Disclaimer', { timeout: 5000 }).scrollIntoView().should('be.visible')
      cy.contains('References', { timeout: 5000 }).scrollIntoView().should('be.visible')
      cy.contains('level of openness', { timeout: 5000 }).scrollIntoView().should('be.visible')
    })
  })

  describe('Reset Functionality', () => {
    it('should reset form when clicking reset button', () => {
      // Select some answers in dropdowns
      cy.get('select').first().select('2')
      cy.get('select').first().should('have.value', '2')

      // Click reset
      cy.contains('ล้างข้อมูล').click()

      // Form should be cleared (back to default value 0)
      cy.get('select').first().should('have.value', '0')
    })
  })

  describe('API Integration', () => {
    it('should call backend API on form submission', () => {
      // Fill and submit
      cy.get('select').each(($select) => {
        cy.wrap($select).select('2')
      })
      cy.contains('คำนวณผลลัพธ์').click()

      // Check that we get a success response (proves API was called successfully)
      cy.contains('ประมวลผลสำเร็จ', { timeout: 15000 }).should('be.visible')
      
      // Verify results are displayed (proves API returned data)
      cy.contains('%', { timeout: 5000 }).should('be.visible')
    })
  })

  describe('Responsive Design', () => {
    it('should work on mobile viewport', () => {
      cy.viewport('iphone-x')
      cy.contains('LGBTQ+').should('be.visible')
      cy.get('select').first().should('be.visible')
    })

    it('should work on tablet viewport', () => {
      cy.viewport('ipad-2')
      cy.contains('แบบสอบถาม').should('be.visible')
    })
  })
})
