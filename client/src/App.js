// client/src/App.js

import React, { useState } from 'react'; 

import './App.css';

import { BrowserRouter as Router, Route, Routes,Link } from 'react-router-dom';

import { Form, Button,Col, Container, Row } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'react-bootstrap-table-next/dist/react-bootstrap-table2.css';
//import BootstrapTable from 'react-bootstrap-table-next';
//import paginationFactory from 'react-bootstrap-table2-paginator';

import ResultList from './components/ResultList';
import Search from './components/Search';
import axios from 'axios';

function App () {
  
  const [results, setResults] = useState([]);

  const search = async (country,query) => {
    try {
      const response = await axios({
        method: 'get',
        url: 'http://localhost:8003/api/v1/cities/cities/',
        params: {
          country,
          query: query
        }
      });
      setResults(response.data);
    } catch (error) {
      console.error(error);
    }
  };




  function Home() {
    return (
      <div>
         <h1>Project search with elasticsearch</h1>
          <p className='lead'>
            Use the controls below to cities the citie  and filter the results.
          </p>
      </div>
    );
  }
  
  function Cargar() {
    return (
      <div>
      <h1>Cities</h1>
       <p className='lead'>
         Results all Cities pagination.
       </p>
   </div>
   
    );
  }
  function Busqueda() {
    return (
      <Container className='pt-3'>
        <h1>Cities</h1>
        <p className='lead'>
          Use the controls below to cities the citie  and filter the results.
        </p>
        <Row>
          <Col lg={4}>
            <Search search={search} /> 
          </Col>
          <Col lg={8}>
            <ResultList results={results} /> 
          </Col>
        </Row>
    </Container>
    );
  }
  

  return (
  
    <Router>
    <div>
      <ul>
        <li>
          <Link to="/">Home</Link>
        </li>
        <li>
          <Link to="/grid">Grid</Link>
        </li>
        <li>
          <Link to="/busqueda">Busqueda</Link>
        </li>
      </ul>

      <hr />

      {/*
        A <Switch> looks through all its children <Route>
        elements and renders the first one whose path
        matches the current URL. Use a <Switch> any time
        you have multiple routes, but you want only one
        of them to render at a time
      */}
      <Routes>
        <Route exact path='/' element={<Home/>}></Route>
        <Route exact path='/grid' element={<Cargar/>}></Route>
        <Route exact path='/busqueda' element={<Busqueda/>}></Route>
      </Routes>
    </div>
  </Router>
    
    
  );
}




export default App;
