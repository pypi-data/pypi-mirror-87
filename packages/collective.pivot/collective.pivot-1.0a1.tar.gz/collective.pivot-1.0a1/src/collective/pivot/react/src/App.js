import React from 'react';
import FamilyView from './pages/FamilyView';

function App({pivot_url, details_url}) {
  return (
      <FamilyView  pivot_url={pivot_url} details_url={details_url} />
  );
}

export default App;