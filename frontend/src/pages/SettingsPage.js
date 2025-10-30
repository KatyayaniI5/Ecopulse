import React, { useState } from 'react';

const SettingsPage = () => {
  const [settings, setSettings] = useState({
    notifications: true,
    emailUpdates: false,
    darkMode: false,
    language: 'en'
  });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setSettings({
      ...settings,
      [name]: type === 'checkbox' ? checked : value
    });
  };

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Settings</h1>
      <div className="max-w-2xl">
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-xl font-semibold text-gray-900 mb-4">Preferences</h3>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <label className="text-sm font-medium text-gray-700">Push Notifications</label>
                <p className="text-sm text-gray-500">Receive notifications about new recommendations</p>
              </div>
              <input
                type="checkbox"
                name="notifications"
                checked={settings.notifications}
                onChange={handleChange}
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
            </div>
            <div className="flex items-center justify-between">
              <div>
                <label className="text-sm font-medium text-gray-700">Email Updates</label>
                <p className="text-sm text-gray-500">Receive weekly email reports</p>
              </div>
              <input
                type="checkbox"
                name="emailUpdates"
                checked={settings.emailUpdates}
                onChange={handleChange}
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
            </div>
            <div className="flex items-center justify-between">
              <div>
                <label className="text-sm font-medium text-gray-700">Dark Mode</label>
                <p className="text-sm text-gray-500">Use dark theme</p>
              </div>
              <input
                type="checkbox"
                name="darkMode"
                checked={settings.darkMode}
                onChange={handleChange}
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Language</label>
              <select
                name="language"
                value={settings.language}
                onChange={handleChange}
                className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="en">English</option>
                <option value="es">Spanish</option>
                <option value="fr">French</option>
                <option value="de">German</option>
              </select>
            </div>
          </div>
          <div className="mt-6">
            <button className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700">
              Save Settings
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SettingsPage;