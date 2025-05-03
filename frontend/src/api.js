import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:5000';

export const getLocations = async () => {
  return axios.get(`${API_BASE_URL}/locations`);
};

export const findPath = async (start, end) => {
  return axios.post(`${API_BASE_URL}/find_path`, { start, end });
};
