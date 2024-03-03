// import React from 'react';
// import logo from './logo.svg';
import React, { useState, useEffect } from 'react';
import './App.css';
import './index.css';

// MUI
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import { styled } from '@mui/material/styles';
import Paper from '@mui/material/Paper';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell, { tableCellClasses } from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';

// Image Imports
import Logo from './assets/logo.jpg';


// Template Styles
const Item = styled(Paper)(({ theme }) => ({
  backgroundColor: theme.palette.mode === 'dark' ? '#1A2027' : '#fff',
  ...theme.typography.body2,
  padding: theme.spacing(1),
  textAlign: 'center',
  color: theme.palette.text.secondary,
}));

const StyledTableCell = styled(TableCell)(({ theme }) => ({
  [`&.${tableCellClasses.head}`]: {
    backgroundColor: theme.palette.common.black,
    color: theme.palette.common.white,
  },
  [`&.${tableCellClasses.body}`]: {
    fontSize: 14,
  },
}));

const StyledTableRow = styled(TableRow)(({ theme }) => ({
  '&:nth-of-type(odd)': {
    backgroundColor: theme.palette.action.hover,
  },
  // hide last border
  '&:last-child td, &:last-child th': {
    border: 0,
  },
}));

interface FoodItem {
  name: String
  expiry_date: String
}


export default function App() {

  const [foods, setFood] = useState([])
  let FoodList: { string: FoodItem[] }

  useEffect(() => {
    // Hard code the URL of the back-end flask server being used
    fetch("http://ec2-3-106-231-109.ap-southeast-2.compute.amazonaws.com:5000/get_user_items").then(
      res => res.json()
    ).then(
      food => {
        console.log(food)
        setFood(food)
      }
    )

  }, [])

  function renderTable() {
    return foods.map((ele, index) => {
      return (
        <StyledTableRow key={index}>
          <StyledTableCell component="th" scope="row">
            {ele["name"]}
          </StyledTableCell>
          <StyledTableCell>{ele["expiry_date"]}</StyledTableCell>
        </StyledTableRow>
      )
    })
  }

  function getImage() {
    return (
      <img
        // Hard code the URL of the back-end flask server being used
        src={"http://ec2-3-106-231-109.ap-southeast-2.compute.amazonaws.com:5000/get_image"}
        style={{ maxWidth: "100%" }}
      />
    )
  }


  return (
    <React.Fragment>

      <center>
        <h1>
          <img src={Logo} alt="Logo"
            width="9%" height="9%" />
        </h1>
      </center>

      <Container maxWidth="sm">

        <Box component="section">
          {getImage()}
        </Box>
        <TableContainer component={Paper}>
          <Table sx={{ maxWidth: "100%" }} aria-label="List of Food">
            <TableHead>
              <TableRow>
                <StyledTableCell>Food&nbsp;Name</StyledTableCell>
                <StyledTableCell>Expiration&nbsp;Date</StyledTableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {renderTable()}

            </TableBody>
          </Table>

        </TableContainer>
      </Container>

    </React.Fragment>
  );
}