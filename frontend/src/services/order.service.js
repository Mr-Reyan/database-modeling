import { apiFetch } from './auth.service'

const BASE_URL = process.env.NEXT_PUBLIC_API_URL

export const checkoutOrder = async () => {
  const response = await apiFetch(`${BASE_URL}/order/checkout/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
  })

  const data = await response.json().catch(() => ({}))

  if (!response.ok) {
    throw new Error(data.error || data.message || 'Failed to place order')
  }

  return data
}

export const getOrders = async () => {
  const response = await apiFetch(`${BASE_URL}/orders/`, {
    method: 'GET',
  })

  const data = await response.json().catch(() => ({}))

  if (!response.ok) {
    throw new Error(data.error || data.message || 'Failed to fetch orders')
  }

  return data
}
