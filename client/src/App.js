import React, { useState } from 'react';
import './App.css';

function App() {
  const [formData, setFormData] = useState({});

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Form data:', formData);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>User Information Form</h1>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Sample Input:</label>
            <input
              type="text"
              onChange={(e) => setFormData({...formData, sample: e.target.value})}
              placeholder="Enter some information"
            />
          </div>
          <button type="submit">Submit</button>
        </form>
      </header>
    </div>
  );
}

export default App;
