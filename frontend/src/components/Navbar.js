'use client'

import React from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import { ShoppingBag, Search, Menu, UserCircle2 } from 'lucide-react'
import { IntegralCF } from '@/app/layout'
import Link from 'next/link'
import { useQuery } from '@tanstack/react-query'
import { getCart } from '@/services/cart.service'

const Navbar = () => {
  const { data: cart } = useQuery({
    queryKey: ['cart'],
    queryFn: getCart,
    staleTime: 1000 * 30,
  })

  const totalCartCount =
    cart?.items?.reduce((total, item) => total + (item.quantity || 1), 0) || 0

  return (
    <header className="border-b">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center md:justify-center justify-between gap-4">
          <button className="lg:hidden">
            <Menu className="h-6 w-6" />
          </button>

          <Link href="/" className={`${IntegralCF.className}  text-2xl font-bold`}>
            SHOP.CO
          </Link>

          <nav className="hidden lg:flex items-center  min-w-80 gap-5">
            <Link href="/store" className="text-md hover:text-gray-600">
              Store
            </Link>
            {/* <a href="#" >Shop</a> */}
            <a href="#" className="text-md hover:text-gray-600">
              On Sale
            </a>
            <a href="#" className="text-md hover:text-gray-600">
              New Arrivals
            </a>
            <a href="#" className="text-md hover:text-gray-600">
              Brands
            </a>
          </nav>

          <div className="flex items-center md:justify-baseline justify-between md:w-full w-auto gap-4">
            <div className="hidden md:flex items-center w-full max-w-150 bg-gray-100 rounded-full px-4 py-2">
              <Search className="h-4 w-4 text-gray-500" />
              <Input
                type="text"
                placeholder="Search for products..."
                className="border-0 bg-transparent focus-visible:ring-0 focus-visible:ring-offset-0 text-md flex-1 w-auto lg:w-full"
              />
            </div>
            <div className="flex items-center gap-1">
              <Button
                asChild
                className="relative rounded-full h-10 w-10 p-0"
                variant="ghost"
              >
                <Link href="/cart" className="flex items-center justify-center w-full h-full">
                  <ShoppingBag size="20" />
                  {totalCartCount > 0 && (
                    <Badge className="absolute -top-1 -right-1 h-5 min-w-5 px-1 bg-black text-white hover:bg-black flex items-center justify-center text-[10px] font-bold rounded-full">
                      {totalCartCount > 99 ? '99+' : totalCartCount}
                    </Badge>
                  )}
                </Link>
              </Button>
              <Button
                className="relative rounded-full h-10 w-10 p-0"
                variant="ghost"
              >
                <UserCircle2 size="20" />
              </Button>
            </div>
          </div>
        </div>

        {/* Mobile Search */}
        <div className="md:hidden mt-3">
          <div className="flex items-center bg-gray-100 rounded-full px-4 py-2">
            <Search className="h-4 w-4 text-gray-500" />
            <Input
              type="text"
              placeholder="Search for products..."
              className="border-0 bg-transparent focus-visible:ring-0 focus-visible:ring-offset-0 text-sm"
            />
          </div>
        </div>
      </div>
    </header>
  )
}

export default Navbar
