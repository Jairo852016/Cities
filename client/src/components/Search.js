// client/src/components/Search.js

import React, { useState } from 'react';

import axios from 'axios';
import { Formik } from 'formik';
import { Button, Col, Form, Row } from 'react-bootstrap';
import { AsyncTypeahead } from 'react-bootstrap-typeahead';


function Search ({ search }) { 
    const [isLoading, setLoading] = useState(false); // new
    const [options, setOptions] = useState([]); // new
    const citiesSearchWord = async query => {
        if (query.length < 2) {
          setLoading(false);
          setOptions([]);
        } else {
          setLoading(true);
          try {
            const response = await axios({
              method: 'get',
              url: 'http://localhost:8003/api/v1/cities/cities-search-words/',
              params: {
                query: query
              }
            });
            setOptions(response.data);
          } catch(error) {
            console.error(error);
            setOptions([]);
          } finally {
            setLoading(false);
          }
        }
      };
    const onSubmit = async (values, actions) => {
        await search(
            values.country,
            values.query
          );
      };

  return (
    <Formik
      initialValues={{
        country: '',
        query: ''
      }}
      onSubmit={onSubmit}
    >
      {({
        handleChange,
        handleSubmit,
        setFieldValue,
        values
      }) => (
        <Form noValidate onSubmit={handleSubmit}>
          <Form.Group controlId="country">
            <Form.Label>Country</Form.Label>
            <Col>
                <Form.Control
                type="text"
                name="country"
                placeholder="Enter a country (e.g. Colombia)"
                value={values.country}
                onChange={handleChange}
                />
                <Form.Text className="text-muted">
                Filters search results by country.
                </Form.Text>
            </Col>
          </Form.Group>  
          <Form.Group controlId='query'>
            <Form.Label>Query</Form.Label>
            <Col>
                <AsyncTypeahead
                    filterBy={() => true}
                    id="query"
                    isLoading={isLoading}
                    labelKey="word"
                    name="query"
                    onChange={selected => {
                        const value = selected.length > 0 ? selected[0].word : '';
                        setFieldValue('query', value);
                    }}
                    onInputChange={value => setFieldValue('query', value)}
                    onSearch={citiesSearchWord}
                    options={options}
                    placeholder="Enter a search term (e.g. barranquilla)"
                    type="text"
                    value={values.query}
                    />
              <Form.Text className='text-muted'>
                Searches for query in citie and admin_name
              </Form.Text>
            </Col>
          </Form.Group>
          <Form.Group as={Row}>
            <Col>
              <Button type='submit' variant='primary'>Search</Button>
            </Col>
          </Form.Group>
        </Form>
      )}
    </Formik>
  );
}

export default Search;
