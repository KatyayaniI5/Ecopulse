import React from 'react';

const DashboardPage = () => {
  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Carbon Score</h3>
          <p className="text-3xl font-bold text-green-600">85%</p>
          <p className="text-sm text-gray-600">Good environmental impact</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Invoices Processed</h3>
          <p className="text-3xl font-bold text-blue-600">24</p>
          <p className="text-sm text-gray-600">This month</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Recommendations</h3>
          <p className="text-3xl font-bold text-purple-600">12</p>
          <p className="text-sm text-gray-600">Available suggestions</p>
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;