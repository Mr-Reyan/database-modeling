import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Separator } from '@/components/ui/separator'
import { Tag } from 'lucide-react'
import React from 'react'

export default function OrderSummary() {
  return (
    <div className="text-md sm:text-lg p-5  md:min-w-100 flex flex-col justify-between gap-6">
      <p className="font-bold sm:text-2xl text-xl">Order Summary</p>
      <p className="flex justify-between">
        <span className="text-gray-500">Subtotal</span>
        <span className="font-bold">$565</span>
      </p>
      <p className="flex justify-between">
        <span className="text-gray-500">Discount (-20%)</span>
        <span className="font-bold text-red-500">-$113</span>
      </p>
      <p className="flex justify-between">
        <span className="text-gray-500">Delivery Fee</span>
        <span className="font-bold">$15</span>
      </p>
      <Separator />
      <p className="flex justify-between">
        <span className="text-gray-700">Total</span>
        <span className="font-bold">$467</span>
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

        <button className="rounded-full bg-black px-6  sm:text-md text-sm text-white hover:cursor-pointer">
          Apply
        </button>
      </div>
      <Button className="bg-black text-white rounded-full p-6">
        Go To Checkout
      </Button>
    </div>
  )
}
