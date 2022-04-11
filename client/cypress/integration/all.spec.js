// client/cypress/integration/all.spec.js

describe('Cities', function () {
    it('Displays the home page.', function () {
      cy.visit('/');
      cy.get('h1').should('contain', 'Cities');
    });
  });




it('Displays a list of results.', function () {
    //cy.intercept('GET', '**/api/v1/cities/cities/**', { fixture: 'cities.json' }).as('getCities');
    cy.intercept('GET', '**/api/v1/cities/cities/**').as('getCities');
    cy.visit('/');
    cy.get('input#country').type('Colombia'); 
    //cy.get('input#query').type('Barranquilla');
    cy.get('input[placeholder="Enter a search term (e.g. barranquilla)"]')
    .type('Barranquilla');
    cy.get('button').contains('Search').click();
    cy.wait('@getCities');
    cy.get('div.card-title').should('contain', 'Atlántico');
  });


  it('Displays  search words.', function () {
    // Stub server
    //cy.intercept(
    //  'GET', '**/api/v1/cities/cities-search-words/**',
    // { fixture: 'cities_search_words.json' }
    //).as('getCitiesSearchWords');
    cy.intercept('GET', '**/api/v1/cities/cities-search-words/**').as('getCitiesSearchWords');

    cy.visit('/');
    cy.get('input[placeholder="Enter a search term (e.g. barranquilla)"]').type('barranquilla');
    cy.wait('@getCitiesSearchWords');
    cy.get('div#query').should('contain', 'barranquilla');
  });
  