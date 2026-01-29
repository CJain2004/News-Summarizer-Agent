import axios from 'axios';

const API_URL = 'http://localhost:8000';

export const api = axios.create({
    baseURL: API_URL,
});

export const fetchArticles = async (company = null, limit = 50) => {
    try {
        const params = { limit };
        if (company) params.company = company;

        const response = await api.get('/articles', { params });
        return response.data;
    } catch (error) {
        console.error('Error fetching articles:', error);
        return [];
    }
};

export const triggerIngestion = async () => {
    try {
        await api.post('/ingest');
        return true;
    } catch (e) {
        console.error("Ingestion trigger failed", e);
        return false;
    }
}
