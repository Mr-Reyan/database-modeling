'use client'

import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Separator } from '@/components/ui/separator'
import { Tag, Loader2, ArrowRight } from 'lucide-react'
import React from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { getCart } from '@/services/cart.service'
import { checkoutOrder } from '@/services/order.service'
import { toast } from 'sonner'

export default function OrderSummary() {
  const queryClient = useQueryClient()

  const { data: cart, isLoading } = useQuery({
    queryKey: ['cart'],
    queryFn: getCart,
  })

  const placeOrderMutation = useMutation({
    mutationFn: async () => {
      const [result] = await Promise.all([
        checkoutOrder(),
        new Promise((resolve) => setTimeout(resolve, 1000)),
      ])
      return result
    },
    onSuccess: (data) => {
      toast.success(data?.message || 'Order placed successfully!')
      // Invalidate cart and products queries so inventory updates everywhere
      queryClient.invalidateQueries({ queryKey: ['cart'] })
      queryClient.invalidateQueries({ queryKey: ['products'] })
      queryClient.invalidateQueries({ queryKey: ['product'] })
      queryClient.invalidateQueries({ queryKey: ['orders'] })
    },
    onError: (err) => {
      toast.error(err?.message || 'Failed to place order. Please try again.')
    },
  })

  const items = cart?.items || []
  const hasItems = items.length > 0

  const subtotal = items.reduce(
    (sum, item) => sum + Number(item.product?.price || 0) * (item.quantity || 1),
    0
  )

  // As requested: 0% discount and $0 delivery fee
  const discount = 0
  const deliveryFee = 0
  const total = hasItems ? subtotal - discount + deliveryFee : 0

  const handlePlaceOrder = () => {
    if (!hasItems) {
      toast.error('Your cart is empty. Please add items before placing an order!')
      return
    }

    // Client-side pre-check for any out-of-stock items before checkout
    for (const item of items) {
      const sizeStockMap = item.product?.specifications?.size_stock || {}
      const availableStock =
        item.size && sizeStockMap[item.size] !== undefined
          ? sizeStockMap[item.size]
          : (item.product?.stock?.stock ?? 99)

      if (availableStock <= 0) {
        toast.error(
          `Cannot place order: "${item.product?.name || 'Item'}" (${item.size || 'Standard'}) is out of stock. Please remove it from your cart.`
        )
        return
      }

      if (item.quantity > availableStock) {
        toast.error(
          `Cannot place order: "${item.product?.name || 'Item'}" quantity (${item.quantity}) exceeds available stock (${availableStock}).`
        )
        return
      }
    }

    placeOrderMutation.mutate()
  }

  return (
    <div className="text-md sm:text-lg p-5 md:min-w-100 flex flex-col justify-between gap-6">
      <p className="font-bold sm:text-2xl text-xl">Order Summary</p>

      <div className="flex flex-col gap-4">
        <p className="flex justify-between">
          <span className="text-gray-500">Subtotal</span>
          <span className="font-bold">${subtotal.toFixed(2)}</span>
        </p>
        <p className="flex justify-between">
          <span className="text-gray-500">Discount (-0%)</span>
          <span className="font-bold text-gray-500">-${discount.toFixed(2)}</span>
        </p>
        <p className="flex justify-between">
          <span className="text-gray-500">Delivery Fee</span>
          <span className="font-bold text-green-600">
            {deliveryFee === 0 ? 'Free' : `$${deliveryFee.toFixed(2)}`}
          </span>
        </p>
      </div>

      <Separator />

      <p className="flex justify-between items-baseline">
        <span className="text-gray-700 font-medium">Total</span>
        <span className="font-bold text-2xl">${total.toFixed(2)}</span>
      </p>

      <div className="flex gap-2">
        <div className="flex flex-1 items-center rounded-full bg-gray-100 px-3 sm:px-4 py-1 sm:py-2">
          <Tag className="h-4 w-4 text-gray-500" />
          <Input
            type="text"
            placeholder="Add promo code"
            className="flex-1 border-0 bg-transparent sm:text-md text-sm focus-visible:ring-0 focus-visible:ring-offset-0"
          />
        </div>

        <button
          type="button"
          onClick={() => toast.info('Promo code feature coming soon!')}
          className="rounded-full bg-black px-6 sm:text-md text-sm text-white hover:bg-black/80 transition-colors cursor-pointer"
        >
          Apply
        </button>
      </div>

      <Button
        type="button"
        disabled={!hasItems || placeOrderMutation.isPending || isLoading}
        onClick={handlePlaceOrder}
        className="w-full bg-black text-white rounded-full py-6 font-medium text-base hover:bg-black/90 cursor-pointer shadow-md transition-all active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
      >
        {placeOrderMutation.isPending ? (
          <>
            <Loader2 className="w-5 h-5 animate-spin" />
            <span>Placing Order...</span>
          </>
        ) : (
          <>
            <span>Place Order</span>
            <ArrowRight className="w-5 h-5" />
          </>
        )}
      </Button>
    </div>
  )
}
