import { apiFetch } from "./auth.service"

const BASE_URL = process.env.NEXT_PUBLIC_API_URL


export const addToCart = async (data,id) => {
    const response = await apiFetch(`${BASE_URL}/cart/add/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({product_id:id,...data})
    })
    return await response.json()
}

export const getCart = async (data)=>{
    const response = await apiFetch(`${BASE_URL}/cart/`,{
        method:'GET'
    })
    return await response.json()
}


export const updateCart = async (newQuantity,id)=>{
    const response = await apiFetch(`${BASE_URL}/cart/items/${id}/`,{
        method:'PATCH',
        headers:{
            'Content-Type':'application/json'
        },
        body: JSON.stringify({quantity:newQuantity})
    })
    return await response.json()
}

export const deleteCartItem = async (prod_id)=>{
    const response = await apiFetch(`${BASE_URL}/cart/${prod_id}/`,{
        method:'DELETE'
    })
    return await response.json()
}