import React from 'react';

const AISuggestionsPage = () => {
  const suggestions = [
    {
      id: 1,
      title: 'Switch to LED Lighting',
      description: 'Replace traditional lighting with LED bulbs to reduce energy consumption by 75%.',
      impact: 'High',
      category: 'Energy'
    },
    {
      id: 2,
      title: 'Implement Paperless Billing',
      description: 'Move to digital invoicing to reduce paper waste and transportation emissions.',
      impact: 'Medium',
      category: 'Waste'
    },
    {
      id: 3,
      title: 'Optimize Supply Chain Routes',
      description: 'Use route optimization software to reduce fuel consumption in deliveries.',
      impact: 'High',
      category: 'Transportation'
    }
  ];

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">AI Recommendations</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {suggestions.map((suggestion) => (
          <div key={suggestion.id} className="bg-white p-6 rounded-lg shadow">
            <div className="flex justify-between items-start mb-2">
              <h3 className="text-lg font-semibold text-gray-900">{suggestion.title}</h3>
              <span className={`px-2 py-1 text-xs font-semibold rounded ${
                suggestion.impact === 'High' ? 'bg-red-100 text-red-800' :
                suggestion.impact === 'Medium' ? 'bg-yellow-100 text-yellow-800' :
                'bg-green-100 text-green-800'
              }`}>
                {suggestion.impact}
              </span>
            </div>
            <p className="text-gray-600 mb-4">{suggestion.description}</p>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-500">{suggestion.category}</span>
              <button className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700">
                Implement
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default AISuggestionsPage;