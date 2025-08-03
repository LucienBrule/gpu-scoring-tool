import React from "react";

// Main Card component
export const Card: React.FC<{
  className?: string;
  children: React.ReactNode;
}> = ({ className = "", children }) => {
  return (
      <div className={`rounded-lg border bg-card text-card-foreground shadow-sm ${className}`}>
        {children}
      </div>
  );
};

// Card Header component
export const CardHeader: React.FC<{
  className?: string;
  children: React.ReactNode;
}> = ({ className = "", children }) => {
  return (
      <div className={`flex flex-col space-y-1.5 p-6 ${className}`}>
        {children}
      </div>
  );
};

// Card Title component
export const CardTitle: React.FC<{
  className?: string;
  children: React.ReactNode;
}> = ({ className = "", children }) => {
  return (
      <h3 className={`text-2xl font-semibold leading-none tracking-tight ${className}`}>
        {children}
      </h3>
  );
};

// Card Description component
export const CardDescription: React.FC<{
  className?: string;
  children: React.ReactNode;
}> = ({ className = "", children }) => {
  return (
      <p className={`text-sm text-muted-foreground ${className}`}>
        {children}
      </p>
  );
};

// Card Content component
export const CardContent: React.FC<{
  className?: string;
  children: React.ReactNode;
}> = ({ className = "", children }) => {
  return (
      <div className={`p-6 pt-0 ${className}`}>
        {children}
      </div>
  );
};

// Card Footer component (additional component that might be useful)
export const CardFooter: React.FC<{
  className?: string;
  children: React.ReactNode;
}> = ({ className = "", children }) => {
  return (
      <div className={`flex items-center p-6 pt-0 ${className}`}>
        {children}
      </div>
  );
};