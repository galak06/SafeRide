// Test script to verify authentication token persistence
console.log('Testing authentication token persistence...');

// Check if token exists in localStorage
const token = localStorage.getItem('authToken');
const timestamp = localStorage.getItem('authTimestamp');

console.log('Current localStorage state:');
console.log('- authToken:', token ? 'EXISTS' : 'NOT FOUND');
console.log('- authTimestamp:', timestamp ? new Date(parseInt(timestamp)).toLocaleString() : 'NOT FOUND');

if (token) {
    console.log('✅ Token found in localStorage - authentication should persist across page reloads');
    
    // Check if token is expired (24 hours)
    if (timestamp) {
        const tokenAge = Date.now() - parseInt(timestamp);
        const maxAge = 24 * 60 * 60 * 1000; // 24 hours
        const isExpired = tokenAge > maxAge;
        
        console.log(`- Token age: ${Math.round(tokenAge / 1000 / 60)} minutes`);
        console.log(`- Token expired: ${isExpired ? 'YES' : 'NO'}`);
        
        if (isExpired) {
            console.log('⚠️ Token is expired - user will need to login again');
        } else {
            console.log('✅ Token is valid - user should remain authenticated');
        }
    }
} else {
    console.log('❌ No token found in localStorage - user will need to login again');
}

// Test API call to verify token works
if (token) {
    console.log('\nTesting API call with stored token...');
    
    fetch('http://localhost:8000/api/auth/me', {
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        },
        credentials: 'include'
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
    })
    .then(user => {
        console.log('✅ API call successful - user authenticated:', user.email);
    })
    .catch(error => {
        console.log('❌ API call failed:', error.message);
        console.log('Token may be invalid or expired');
    });
} 