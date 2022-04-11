// client/src/components/ResultList.js

import React from 'react';

import { sanitize } from 'dompurify'; 
import { Card } from 'react-bootstrap'; 


function ResultList ({ results }) {
  
  const resultItems = results.map(result =>
    <Card className='mb-3' key={result.id}>
      <Card.Body>
        <Card.Title
          dangerouslySetInnerHTML={{
            __html: `${sanitize(result.citie)} ${sanitize(result.admin_name)}`
          }}
        ></Card.Title>
        <Card.Subtitle
          className='mb-2 text-muted'
        >{result.country} | Capital {result.capital}  
        </Card.Subtitle>
        <Card.Text dangerouslySetInnerHTML={{ __html: sanitize(result.population) }} />
      </Card.Body>
    </Card>
  );


  return (
    <div>
      {!results && <p>Search using the left panel.</p>}
      {results && results.length === 0 && <p>No results found.</p>}
      {resultItems}
    </div>
  );
}

export default ResultList;
