// import React from 'react';
// import logo from './logo.svg';
import React , { useState } from 'react';
import './App.css';
import './index.css';

interface FoodItem {
  id: Number,
  name: String,
  expiry_date: String
}

interface Fridge {
  items: FoodItem[];
}

function MyButton() {
  return (
    <button>Testing</button>
  )
}

interface PropsType {
  children: React.ReactNode;
}

function ListView(props: PropsType) {
  return (
    <ul>
      {React.Children.map(props.children, (child) => {
        return <li>{child}</li>;
      })}
    </ul>
  );
}

export default function App() {

  const [foods, setFoods] = useState([
    { id: 1, name: "Banana", expiry_date: "05/03/2024"},
    { id: 2, name: "Apple", expiry_date: "07/03/2024"},
    { id: 3, name: "Orange", expiry_date: "08/03/2024"}
  ]);

  return (
    <div className="container">
        <h3 className="p-3 text-center">React - Display a list of items</h3>
        <table className="table table-striped table-bordered">
            <thead>
                <tr>
                    <th>Food</th>
                    <th>Expire Date</th>
                </tr>
            </thead>
            <tbody>
                {foods && foods.map(food =>
                    <tr key={food.id}>
                        <td>{food.name}</td>
                        <td>{food.expiry_date}</td>
                    </tr>
                )}
            </tbody>
        </table>
    </div>
);
}