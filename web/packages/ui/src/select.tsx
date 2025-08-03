"use client";

import React, {createContext, useContext, useState, forwardRef} from "react";

// Context to manage select state
interface SelectContextType {
    value: string;
    onValueChange: (value: string) => void;
    open: boolean;
    setOpen: (open: boolean) => void;
}

const SelectContext = createContext<SelectContextType | undefined>(undefined);

// Hook to use select context
const useSelectContext = () => {
    const context = useContext(SelectContext);
    if (!context) {
        throw new Error("Select components must be used within a Select provider");
    }
    return context;
};

// Main Select component
interface SelectProps {
    value?: string;
    defaultValue?: string;
    onValueChange?: (value: string) => void;
    disabled?: boolean;
    name?: string;
    children: React.ReactNode;
    className?: string;
}

export function Select({
                           value,
                           defaultValue = "",
                           onValueChange,
                           disabled = false,
                           name,
                           children,
                           className = "",
                       }: SelectProps) {
    // Use controlled or uncontrolled state
    const [selectValue, setSelectValue] = useState(defaultValue);
    const [open, setOpen] = useState(false);

    // Determine if component is controlled or uncontrolled
    const isControlled = value !== undefined;
    const currentValue = isControlled ? value : selectValue;

    const handleValueChange = (newValue: string) => {
        if (!isControlled) {
            setSelectValue(newValue);
        }
        onValueChange?.(newValue);
        setOpen(false);
    };

    return (
        <SelectContext.Provider value={{value: currentValue, onValueChange: handleValueChange, open, setOpen}}>
            <div className={`relative ${className}`}>
                {children}
                {name && (
                    <input type="hidden" name={name} value={currentValue}/>
                )}
            </div>
        </SelectContext.Provider>
    );
}

// SelectTrigger component
interface SelectTriggerProps {
    className?: string;
    children: React.ReactNode;
}

interface SelectTriggerProps {
    id?: string
}

export const SelectTrigger = forwardRef<HTMLButtonElement, SelectTriggerProps>(
    ({className = "", children, id}, ref) => {
        const {value, open, setOpen} = useSelectContext();

        return (
            <button
                type="button"
                ref={ref}
                onClick={() => setOpen(!open)}
                aria-haspopup="listbox"
                aria-expanded={open}
                className={`flex h-10 w-full items-center justify-between rounded-md border border-gray-300 bg-white px-3 py-2 text-sm ring-offset-white placeholder:text-gray-500 focus:outline-none focus:ring-2 focus:ring-gray-950 focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 dark:border-gray-700 dark:bg-gray-950 dark:ring-offset-gray-950 dark:placeholder:text-gray-400 dark:focus:ring-gray-300 ${className}`}
            >
                {children}
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="24"
                    height="24"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    className="h-4 w-4 opacity-50"
                >
                    <path d="m6 9 6 6 6-6"/>
                </svg>
            </button>
        );
    }
);
SelectTrigger.displayName = "SelectTrigger";

// SelectValue component
interface SelectValueProps {
    placeholder?: string;
    className?: string;
}

export function SelectValue({placeholder = "Select an option", className = ""}: SelectValueProps) {
    const {value} = useSelectContext();

    return (
        <span className={`block truncate ${value ? "" : "text-gray-500 dark:text-gray-400"} ${className}`}>
      {value || placeholder}
    </span>
    );
}

// SelectContent component
interface SelectContentProps {
    className?: string;
    children: React.ReactNode;
}

export function SelectContent({className = "", children}: SelectContentProps) {
    const {open} = useSelectContext();

    if (!open) return null;

    return (
        <div className="relative z-50">
            <div className="fixed inset-0" onClick={() => useSelectContext().setOpen(false)}/>
            <div
                className={`absolute left-0 top-full mt-1 w-full overflow-hidden rounded-md border border-gray-200 bg-white shadow-md dark:border-gray-800 dark:bg-gray-950 ${className}`}>
                <div className="max-h-60 overflow-auto p-1">
                    {children}
                </div>
            </div>
        </div>
    );
}

// SelectItem component
interface SelectItemProps {
    value: string;
    disabled?: boolean;
    className?: string;
    children: React.ReactNode;
}

export function SelectItem({value, disabled = false, className = "", children}: SelectItemProps) {
    const {value: selectedValue, onValueChange} = useSelectContext();
    const isSelected = selectedValue === value;

    return (
        <div
            role="option"
            aria-selected={isSelected}
            data-value={value}
            data-disabled={disabled}
            onClick={() => {
                if (!disabled) {
                    onValueChange(value);
                }
            }}
            className={`relative flex w-full cursor-default select-none items-center rounded-sm py-1.5 pl-8 pr-2 text-sm outline-none ${
                isSelected
                    ? "bg-gray-100 text-gray-900 dark:bg-gray-800 dark:text-gray-50"
                    : "text-gray-700 dark:text-gray-400"
            } ${
                disabled
                    ? "pointer-events-none opacity-50"
                    : "cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-800"
            } ${className}`}
        >
      <span className="absolute left-2 flex h-3.5 w-3.5 items-center justify-center">
        {isSelected && (
            <svg
                xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
                className="h-4 w-4"
            >
                <path d="M5 12l5 5 9-9"/>
            </svg>
        )}
      </span>
            <span className="truncate">{children}</span>
        </div>
    );
}