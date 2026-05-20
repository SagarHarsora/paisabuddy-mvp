import React from 'react'

function App() {
  return (
    <div className="min-h-screen bg-white">
      {/* Header */}
      <header className="bg-blue-900 text-white py-6 px-4">
        <div className="max-w-6xl mx-auto">
          <h1 className="text-3xl font-bold">PaisaBuddy</h1>
          <p className="text-blue-200">Monthly financial clarity for salaried Indians</p>
        </div>
      </header>

      {/* Hero Section */}
      <section className="bg-gradient-to-r from-blue-50 to-yellow-50 py-12 px-4">
        <div className="max-w-6xl mx-auto text-center">
          <h2 className="text-4xl font-bold mb-4">Understand Your Money</h2>
          <p className="text-xl text-gray-700 mb-8">
            Upload your bank statement. Get instant insights about your spending habits.
          </p>
          <button className="bg-blue-900 text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-800">
            Get Started
          </button>
        </div>
      </section>

      {/* Features */}
      <section className="py-12 px-4">
        <div className="max-w-6xl mx-auto">
          <h3 className="text-3xl font-bold mb-8 text-center">Features</h3>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="p-6 border rounded-lg">
              <h4 className="text-xl font-semibold mb-2">📊 Smart Analysis</h4>
              <p className="text-gray-700">Automatically categorize your spending into food, transport, shopping, and more.</p>
            </div>
            <div className="p-6 border rounded-lg">
              <h4 className="text-xl font-semibold mb-2">📈 Paisa Score</h4>
              <p className="text-gray-700">Get a 0-100 score based on your savings rate, spending patterns, and financial health.</p>
            </div>
            <div className="p-6 border rounded-lg">
              <h4 className="text-xl font-semibold mb-2">💡 Insights</h4>
              <p className="text-gray-700">Receive personalized recommendations to improve your financial habits.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Sample Report */}
      <section className="bg-gray-50 py-12 px-4">
        <div className="max-w-6xl mx-auto">
          <h3 className="text-3xl font-bold mb-8 text-center">Sample Report</h3>
          <div className="bg-white p-8 rounded-lg shadow-lg">
            <div className="grid md:grid-cols-2 gap-8">
              <div>
                <h4 className="text-2xl font-bold text-blue-900 mb-4">Your Paisa Score: 72</h4>
                <p className="text-gray-700 mb-4">
                  "Excellent financial control this month! You saved 32% of your income. 
                  Food and dining is taking 18% of your expenses. Consider meal planning to reduce costs."
                </p>
                <div className="space-y-3">
                  <div className="flex justify-between">
                    <span>Total Income</span>
                    <span className="font-semibold">₹75,000</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Total Expense</span>
                    <span className="font-semibold">₹51,000</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Savings</span>
                    <span className="font-semibold text-green-600">₹24,000 (32%)</span>
                  </div>
                </div>
              </div>
              <div>
                <h4 className="font-semibold mb-4">Spending Breakdown</h4>
                <div className="space-y-3">
                  <div>
                    <div className="flex justify-between mb-1">
                      <span>Food & Dining</span>
                      <span>₹9,180 (18%)</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded h-2">
                      <div className="bg-red-500 h-2 rounded" style={{width: '18%'}}></div>
                    </div>
                  </div>
                  <div>
                    <div className="flex justify-between mb-1">
                      <span>Transport</span>
                      <span>₹4,080 (8%)</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded h-2">
                      <div className="bg-orange-500 h-2 rounded" style={{width: '8%'}}></div>
                    </div>
                  </div>
                  <div>
                    <div className="flex justify-between mb-1">
                      <span>Shopping</span>
                      <span>₹6,120 (12%)</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded h-2">
                      <div className="bg-yellow-500 h-2 rounded" style={{width: '12%'}}></div>
                    </div>
                  </div>
                  <div>
                    <div className="flex justify-between mb-1">
                      <span>Bills & Utilities</span>
                      <span>₹3,060 (6%)</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded h-2">
                      <div className="bg-blue-500 h-2 rounded" style={{width: '6%'}}></div>
                    </div>
                  </div>
                  <div>
                    <div className="flex justify-between mb-1">
                      <span>EMI & Loans</span>
                      <span>₹12,500 (25%)</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded h-2">
                      <div className="bg-purple-500 h-2 rounded" style={{width: '25%'}}></div>
                    </div>
                  </div>
                  <div>
                    <div className="flex justify-between mb-1">
                      <span>Other</span>
                      <span>₹16,060 (31%)</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded h-2">
                      <div className="bg-gray-500 h-2 rounded" style={{width: '31%'}}></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="bg-blue-900 text-white py-12 px-4">
        <div className="max-w-6xl mx-auto text-center">
          <h3 className="text-3xl font-bold mb-4">Ready to understand your finances?</h3>
          <p className="text-blue-100 mb-8">Upload your bank statement to see your Paisa Score and monthly insights.</p>
          <button className="bg-white text-blue-900 px-8 py-3 rounded-lg font-semibold hover:bg-blue-50">
            Upload Now
          </button>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-gray-300 py-8 px-4">
        <div className="max-w-6xl mx-auto text-center">
          <p>&copy; 2024 PaisaBuddy. All rights reserved.</p>
          <p className="text-sm mt-2">Your financial data is encrypted and deleted within 60 days.</p>
        </div>
      </footer>
    </div>
  )
}

export default App
