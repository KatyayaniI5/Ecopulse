import React, { useState } from 'react';

const WhatIfSimulatorPage = () => {
  const [scenario, setScenario] = useState({
    energyReduction: 20,
    wasteReduction: 15,
    transportOptimization: 25
  });

  const handleChange = (e) => {
    setScenario({
      ...scenario,
      [e.target.name]: parseInt(e.target.value)
    });
  };

  const calculateImpact = () => {
    const baseScore = 85;
    const energyImpact = (scenario.energyReduction * 0.3);
    const wasteImpact = (scenario.wasteReduction * 0.2);
    const transportImpact = (scenario.transportOptimization * 0.25);
    
    return Math.min(100, baseScore + energyImpact + wasteImpact + transportImpact);
  };

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">What-If Simulator</h1>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-xl font-semibold text-gray-900 mb-4">Scenario Parameters</h3>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Energy Reduction (%)
              </label>
              <input
                type="range"
                name="energyReduction"
                min="0"
                max="50"
                value={scenario.energyReduction}
                onChange={handleChange}
                className="w-full"
              />
              <span className="text-sm text-gray-600">{scenario.energyReduction}%</span>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Waste Reduction (%)
              </label>
              <input
                type="range"
                name="wasteReduction"
                min="0"
                max="50"
                value={scenario.wasteReduction}
                onChange={handleChange}
                className="w-full"
              />
              <span className="text-sm text-gray-600">{scenario.wasteReduction}%</span>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Transport Optimization (%)
              </label>
              <input
                type="range"
                name="transportOptimization"
                min="0"
                max="50"
                value={scenario.transportOptimization}
                onChange={handleChange}
                className="w-full"
              />
              <span className="text-sm text-gray-600">{scenario.transportOptimization}%</span>
            </div>
          </div>
        </div>
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-xl font-semibold text-gray-900 mb-4">Projected Impact</h3>
          <div className="text-center">
            <div className="text-6xl font-bold text-green-600 mb-2">
              {calculateImpact().toFixed(1)}%
            </div>
            <p className="text-gray-600">New Carbon Score</p>
            <div className="mt-4 p-4 bg-green-50 rounded-lg">
              <p className="text-sm text-green-800">
                This scenario would improve your environmental impact by{' '}
                <span className="font-semibold">
                  {(calculateImpact() - 85).toFixed(1)}%
                </span>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default WhatIfSimulatorPage;