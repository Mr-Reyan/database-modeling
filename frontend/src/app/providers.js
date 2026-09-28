'use client';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useEffect, useState } from 'react';
// import { ThemeProvider } from 'next-themes';
export default function Providers({children}) {
  const [queryClient] = useState(() =>
      new QueryClient({
        defaultOptions: {
          queries: {
            staleTime: 5 * 60 * 1000,
          },
        },
      })
  );

  useEffect(()=>{
    fetch('http://127.0.0.1:8000/csrf/',{
      credentials:'include'
    })
  },[])

  return (
    <QueryClientProvider client={queryClient}>
      {/* <ThemeProvider
      attribute="class"
      defaultTheme="system"
      enableSystem
      disableTransitionOnChange
    >
      {children}
    </ThemeProvider> */}
    {children}
    </QueryClientProvider>
  )
}