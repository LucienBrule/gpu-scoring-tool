'use client';
import {QueryClientProvider} from '@tanstack/react-query';
import {ReactNode, useEffect, useState} from 'react';
import {getQueryClient} from "@/components/Queries";

interface ProvidersProps {
  children: ReactNode;
}

export default function Providers({ children }: ProvidersProps) {
  const [queryClient,setQueryClient] = useState(() => getQueryClient());

  useEffect(() => {
    console.log('queryClient', queryClient);

  }, [queryClient])
  console.log('queryClient', queryClient);
  return (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );
}