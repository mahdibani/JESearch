import { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [query, setQuery] = useState('');  // Search query state
  const [results, setResults] = useState([]);  // Search results state
  const [loading, setLoading] = useState(false);  // Loading state
  const [error, setError] = useState(null);  // Error state
  const [compareResults, setCompareResults] = useState(null);  // Compare results state
  const [loadingCompare, setLoadingCompare] = useState(false);  // Loading state for comparison
  const [selectedEnterprise, setSelectedEnterprise] = useState(null);  // Selected enterprise for details
  const [generatedMessage, setGeneratedMessage] = useState(null);
  const [loadingMessage, setLoadingMessage] = useState(false);

  // Function to handle search and API request
  const handleSearch = async () => {
    setLoading(true);
    setError(null);
    try {
      // Make the API call to your FastAPI backend
      const response = await axios.post('http://localhost:8008/search_junior_enterprises', {
        query: query
      });
      // Set the search results from the response
      setResults(response.data.enterprises);
    } catch (err) {
      // Handle error case
      setError('Failed to fetch data. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  // Function to handle the compare action
  const handleCompare = async (enterprise) => {
    setLoadingCompare(true);
    setCompareResults(null);
    try {
      const response = await axios.post('http://localhost:8099/compare_junior_enterprise', {
        services: enterprise.services || "",
        description: enterprise.description || "",
        name: enterprise.name || ""
      }, {
        headers: {
          'Content-Type': 'application/json'
        }
      });
      setCompareResults(response.data);
      setError(null);
    } catch (error) {
      const errorMessage = error.response?.data?.detail || 'Comparison failed. Please check the enterprise data.';
      setError(errorMessage);
      console.error("Comparison error:", error.response?.data);
    } finally {
      setLoadingCompare(false);
    }
  };
  // Add message generation handler
  const handleGenerateMessage = async () => {
    setLoadingMessage(true);
    try {
      const response = await axios.post('http://localhost:8066/generate_collaboration_message', {
        je_name: compareResults.jeName,
        je_services: compareResults.jeServices,
        je_description: compareResults.jeDescription,
        recommendations: compareResults.recommendations
      }, {
        headers: {
          'Content-Type': 'application/json'
        }
      });
      
      setGeneratedMessage(response.data.message);
      setError(null);
    } catch (error) {
      let errorMsg = 'Failed to generate message. Please try again.';
      
      if (error.response?.data?.detail) {
        // Handle Pydantic validation errors
        if (Array.isArray(error.response.data.detail)) {
          errorMsg = error.response.data.detail.map(e => e.msg).join(', ');
        } else {
          errorMsg = error.response.data.detail;
        }
      }
      
      setError(errorMsg);
    } finally {
      setLoadingMessage(false);
    }
  };
  // Function to handle the view details action
  const handleViewDetails = (enterprise) => {
    setSelectedEnterprise((prev) => (prev && prev.name === enterprise.name ? null : enterprise));
  };

  return (
    <div className="App">
      <h1>Junior Enterprise Search</h1>

      {/* Search Input */}
      <div className="search-bar">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search by name, service, or country"
        />
        <button onClick={handleSearch} disabled={loading}>
          {loading ? 'Searching...' : 'Search'}
        </button>
      </div>

      {/* Error Handling */}
      {error && <div className="error">{error}</div>}

      {/* Display Search Results in Grid */}
      {results.length > 0 && (
        <div className="results">
          <h2>Search Results:</h2>
          <div className="enterprise-grid">
            {results.map((enterprise, index) => (
              <div key={index} className="enterprise">
                <h3>{enterprise.name}</h3>
                <p><strong>Country:</strong> {enterprise.country}</p>
                {!selectedEnterprise || selectedEnterprise.name !== enterprise.name ? (
                  <>
                    <p><strong>Services:</strong> {enterprise.services}</p>
                    <p><strong>Description:</strong> {enterprise.description}</p>
                  </>
                ) : null}
                <a href={enterprise.website} target="_blank" rel="noopener noreferrer">Website</a><br />
                <a href={enterprise.facebook} target="_blank" rel="noopener noreferrer">Facebook</a><br />
                <a href={enterprise.instagram} target="_blank" rel="noopener noreferrer">Instagram</a><br />
                <a href={enterprise.linkedin} target="_blank" rel="noopener noreferrer">LinkedIn</a><br />
                <a href={`mailto:${enterprise.email}`}>Email</a><br />

                <button onClick={() => handleViewDetails(enterprise)} className="view-details-button">
                  View Details
                </button>

                <button onClick={() => handleCompare(enterprise)} className="compare-button">
                  Compare with our beloved JE 🥰
                </button>

                {selectedEnterprise && selectedEnterprise.name === enterprise.name && (
                  <div className="details-container">
                    <div className="enterprise-details">
                      <h4>Details of {selectedEnterprise.name}</h4>
                      <div className="card">
                        <h5>Services:</h5>
                        <p>{selectedEnterprise.services}</p>
                        <h5>Description:</h5>
                        <p>{selectedEnterprise.description}</p>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {results.length === 0 && !loading && <p>No results found.</p>}
      
      {compareResults && (
  <>
    <div className="comparison-overlay" onClick={() => setCompareResults(null)} />
    <div className="comparison-card">
      <button className="close-button" onClick={() => setCompareResults(null)}>
        &times;
      </button>
      <h3>Comparison: {compareResults.jeName || 'Unknown JE'} vs Inceptum JE</h3>
      <p><strong>Similarity Score:</strong> {compareResults.similarity_score}%</p>
      <h4>Recommendations:</h4>
      <p>{compareResults.recommendations || 'No recommendations available'}</p>
      <button 
        className="generate-message-button"
        onClick={handleGenerateMessage}
        disabled={loadingMessage || !compareResults.jeName}
      >
        {loadingMessage ? 'Generating...' : 'Generate Collaboration Message ✉️'}
      </button>
    </div>
  </>
)}
  {generatedMessage && (
    <>
      <div className="comparison-overlay" onClick={() => setGeneratedMessage(null)} />
      <div className="comparison-card">
        <button className="close-button" onClick={() => setGeneratedMessage(null)}>
          &times;
        </button>
        <h3>Collaboration Message Template</h3>
        <div className="email-content">
          {generatedMessage.split('\n').map((line, index) => (
            <p key={index}>{line}</p>
          ))}
        </div>
        <button 
          className="generate-message-button"
          onClick={() => navigator.clipboard.writeText(generatedMessage)}
        >
          Copy to Clipboard 📋
        </button>
      </div>
    </>
  )}

    </div>
  );
}

export default App;
