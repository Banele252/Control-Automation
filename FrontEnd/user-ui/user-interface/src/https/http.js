
export async function fetchExceptionsHTTP () {
    const response = await fetch('http://localhost:' + import.meta.env.VITE_BACKEND_PORT + '/supabase/data/exception')
    const exceptions = await response.json()
    
    if(!response.ok) {
        const error = new Error('Failed to fetch exceptions')
        throw error
    }
    return exceptions
}

export async function fetchChatResponseHTTP(userMessage){
    const response = await fetch('http://localhost:' + import.meta.env.VITE_BACKEND_PORT + '/interactive-agent/interactive-agent?message=' + encodeURIComponent(userMessage), {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        }
    )
    const chatResponse = await response.json()
    if(!response.ok) {
        const error = new Error('Failed to fetch chat response')
        throw error
    }
    return chatResponse
}