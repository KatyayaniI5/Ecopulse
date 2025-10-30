import React from 'react';

const CarbonScorePage = () => {
  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Carbon Score</h1>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-xl font-semibold text-gray-900 mb-4">Current Score</h3>
          <div className="text-center">
            <div className="text-6xl font-bold text-green-600 mb-2">85%</div>
            <p className="text-gray-600">Excellent environmental impact</p>
          </div>
        </div>
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-xl font-semibold text-gray-900 mb-4">Breakdown</h3>
          <div className="space-y-3">
            <div className="flex justify-between">
              <span>Energy Usage</span>
              <span className="font-semibold text-green-600">90%</span>
            </div>
            <div className="flex justify-between">
              <span>Waste Management</span>
              <span className="font-semibold text-blue-600">85%</span>
            </div>
            <div className="flex justify-between">
              <span>Supply Chain</span>
              <span className="font-semibold text-yellow-600">75%</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CarbonScorePage;