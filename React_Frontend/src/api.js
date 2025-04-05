import axios from "axios";

// Configure base URLs for different services
const SEARCH_API = "http://localhost:8008";
const COMPARE_API = "http://localhost:8099";
const GENERATE_API = "http://localhost:8066";

export const searchJuniorEnterprises = async (query) => {
  try {
    const response = await axios.post(`${SEARCH_API}/search_junior_enterprises`, { query });
    return { data: response.data, error: null };
  } catch (error) {
    console.error("Search error:", error.response?.data || error.message);
    return { data: null, error: error.response?.data?.detail || "Failed to search" };
  }
};

export const compareJuniorEnterprise = async (enterprise) => {
  try {
    const response = await axios.post(`${COMPARE_API}/compare_junior_enterprise`, {
      name: enterprise.name || "",
      services: enterprise.services || "",
      description: enterprise.description || ""
    });
    return { data: response.data, error: null };
  } catch (error) {
    console.error("Compare error:", error.response?.data || error.message);
    return { data: null, error: error.response?.data?.detail || "Comparison failed" };
  }
};

export const generateCollaborationMessage = async (compareData) => {
  try {
    const response = await axios.post(`${GENERATE_API}/generate_collaboration_message`, {
      je_name: compareData.jeName,
      je_services: compareData.jeServices,
      je_description: compareData.jeDescription,
      recommendations: compareData.recommendations
    });
    return { data: response.data, error: null };
  } catch (error) {
    console.error("Generate error:", error.response?.data || error.message);
    return { data: null, error: error.response?.data?.detail || "Message generation failed" };
  }
};

// Utility function for clipboard operations
export const copyToClipboard = async (text) => {
  try {
    await navigator.clipboard.writeText(text);
    return { success: true, error: null };
  } catch (error) {
    console.error("Copy error:", error);
    return { success: false, error: "Failed to copy to clipboard" };
  }
};