// Import the axios library to make HTTP requests
const axios = require('axios');

// Define your Netlify function
exports.handler = async (event, context) => {
    try {
        // Make a GET request to your Flask app's endpoint
        const response = await axios.get('https://your-flask-app-url/api/data');

        // Extract and return data from the Flask app's response
        const data = response.data;
        return {
            statusCode: 200,
            body: JSON.stringify(data)
        };
    } catch (error) {
        // Handle any errors
        console.error('Error fetching data:', error);
        return {
            statusCode: 500,
            body: JSON.stringify({ error: 'Internal Server Error' })
        };
    }
};
