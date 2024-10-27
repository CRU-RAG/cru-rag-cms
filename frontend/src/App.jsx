import { useState } from 'react'
import DataTable from './Components/DataTable';
import Header from './Components/Header';
import DashBoard from './Components/DashBoard';
import TopBar from './Components/TopBar';
function App() {
  return (
    <div className="flex min-h-screen">
      {/* Sidebar (Dashboard) - 25% width */}
      <DashBoard />

      {/* Main Content (Header and DataTable) - 75% width */}
      <div className="flex flex-col w-3/4 h-screen overflow-y-scroll">
        <TopBar />
        <Header />
        <DataTable />
      </div>
    </div>
  );
}

export default App;


