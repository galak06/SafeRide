// TypeScript interfaces for validation - follows Interface Segregation Principle
export interface ValidationRule {
  test: (value: string) => boolean;
  message: string;
}

export interface ValidationResult {
  isValid: boolean;
  message: string;
}

export interface FieldValidation {
  [fieldName: string]: ValidationResult;
}

// TypeScript interface for form validation - follows Single Responsibility Principle
export interface FormValidation {
  isValid: boolean;
  errors: FieldValidation;
}

// Constants for validation patterns - follows DRY principle
const VALIDATION_PATTERNS = {
  EMAIL: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
  PHONE: /^\+?[\d\s\-\(\)]{10,}$/,
  PASSWORD: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/,
  NAME: /^[a-zA-Z\s]{2,50}$/,
  ZIP_CODE: /^\d{5}(-\d{4})?$/
} as const;

// Validation rules following Strategy pattern
export const validationRules = {
  required: (fieldName: string): ValidationRule => ({
    test: (value: string) => value.trim().length > 0,
    message: `${fieldName} is required`
  }),

  email: (): ValidationRule => ({
    test: (value: string) => VALIDATION_PATTERNS.EMAIL.test(value),
    message: 'Please enter a valid email address'
  }),

  phone: (): ValidationRule => ({
    test: (value: string) => VALIDATION_PATTERNS.PHONE.test(value),
    message: 'Please enter a valid phone number'
  }),

  password: (): ValidationRule => ({
    test: (value: string) => VALIDATION_PATTERNS.PASSWORD.test(value),
    message: 'Password must be at least 8 characters with uppercase, lowercase, number, and special character'
  }),

  passwordConfirm: (password: string): ValidationRule => ({
    test: (value: string) => value === password,
    message: 'Passwords do not match'
  }),

  minLength: (min: number): ValidationRule => ({
    test: (value: string) => value.length >= min,
    message: `Must be at least ${min} characters long`
  }),

  maxLength: (max: number): ValidationRule => ({
    test: (value: string) => value.length <= max,
    message: `Must be no more than ${max} characters long`
  }),

  name: (): ValidationRule => ({
    test: (value: string) => VALIDATION_PATTERNS.NAME.test(value),
    message: 'Please enter a valid name (2-50 characters, letters and spaces only)'
  }),

  zipCode: (): ValidationRule => ({
    test: (value: string) => VALIDATION_PATTERNS.ZIP_CODE.test(value),
    message: 'Please enter a valid ZIP code'
  }),

  numeric: (): ValidationRule => ({
    test: (value: string) => /^\d+$/.test(value),
    message: 'Must contain only numbers'
  }),

  positiveNumber: (): ValidationRule => ({
    test: (value: string) => {
      const num = parseFloat(value);
      return !isNaN(num) && num > 0;
    },
    message: 'Must be a positive number'
  }),

  url: (): ValidationRule => ({
    test: (value: string) => {
      try {
        new URL(value);
        return true;
      } catch {
        return false;
      }
    },
    message: 'Please enter a valid URL'
  }),

  date: (): ValidationRule => ({
    test: (value: string) => {
      const date = new Date(value);
      return !isNaN(date.getTime());
    },
    message: 'Please enter a valid date'
  }),

  futureDate: (): ValidationRule => ({
    test: (value: string) => {
      const date = new Date(value);
      return !isNaN(date.getTime()) && date > new Date();
    },
    message: 'Date must be in the future'
  }),

  pastDate: (): ValidationRule => ({
    test: (value: string) => {
      const date = new Date(value);
      return !isNaN(date.getTime()) && date < new Date();
    },
    message: 'Date must be in the past'
  })
};

/**
 * Validates a single field value against multiple rules
 * Follows Single Responsibility Principle
 */
export const validateField = (value: string, rules: ValidationRule[]): ValidationResult => {
  for (const rule of rules) {
    if (!rule.test(value)) {
      return {
        isValid: false,
        message: rule.message
      };
    }
  }

  return {
    isValid: true,
    message: ''
  };
};

/**
 * Validates an entire form object
 * Follows Single Responsibility Principle
 */
export const validateForm = (formData: Record<string, string>, fieldRules: Record<string, ValidationRule[]>): FormValidation => {
  const errors: FieldValidation = {};
  let isValid = true;

  for (const [fieldName, rules] of Object.entries(fieldRules)) {
    const value = formData[fieldName] || '';
    const result = validateField(value, rules);
    
    if (!result.isValid) {
      errors[fieldName] = result;
      isValid = false;
    }
  }

  return {
    isValid,
    errors
  };
};

/**
 * Validates email format
 * Follows Single Responsibility Principle
 */
export const isValidEmail = (email: string): boolean => {
  return VALIDATION_PATTERNS.EMAIL.test(email);
};

/**
 * Validates phone number format
 * Follows Single Responsibility Principle
 */
export const isValidPhone = (phone: string): boolean => {
  return VALIDATION_PATTERNS.PHONE.test(phone);
};

/**
 * Validates password strength
 * Follows Single Responsibility Principle
 */
export const isValidPassword = (password: string): boolean => {
  return VALIDATION_PATTERNS.PASSWORD.test(password);
};

/**
 * Validates name format
 * Follows Single Responsibility Principle
 */
export const isValidName = (name: string): boolean => {
  return VALIDATION_PATTERNS.NAME.test(name);
};

/**
 * Validates ZIP code format
 * Follows Single Responsibility Principle
 */
export const isValidZipCode = (zipCode: string): boolean => {
  return VALIDATION_PATTERNS.ZIP_CODE.test(zipCode);
};

/**
 * Sanitizes input by removing dangerous characters
 * Follows Single Responsibility Principle
 */
export const sanitizeInput = (input: string): string => {
  return input
    .trim()
    .replace(/[<>]/g, '') // Remove potential HTML tags
    .replace(/javascript:/gi, '') // Remove javascript: protocol
    .replace(/on\w+=/gi, ''); // Remove event handlers
};

/**
 * Formats phone number for display
 * Follows Single Responsibility Principle
 */
export const formatPhoneNumber = (phone: string): string => {
  const cleaned = phone.replace(/\D/g, '');
  
  if (cleaned.length === 10) {
    return `(${cleaned.slice(0, 3)}) ${cleaned.slice(3, 6)}-${cleaned.slice(6)}`;
  } else if (cleaned.length === 11 && cleaned.startsWith('1')) {
    return `+1 (${cleaned.slice(1, 4)}) ${cleaned.slice(4, 7)}-${cleaned.slice(7)}`;
  }
  
  return phone;
};

/**
 * Formats date for display
 * Follows Single Responsibility Principle
 */
export const formatDate = (date: string | Date): string => {
  const dateObj = typeof date === 'string' ? new Date(date) : date;
  
  if (isNaN(dateObj.getTime())) {
    return '';
  }
  
  return dateObj.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
};

/**
 * Formats currency for display
 * Follows Single Responsibility Principle
 */
export const formatCurrency = (amount: number, currency: string = 'USD'): string => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency
  }).format(amount);
};

/**
 * Validates and formats credit card number
 * Follows Single Responsibility Principle
 */
export const formatCreditCard = (cardNumber: string): string => {
  const cleaned = cardNumber.replace(/\D/g, '');
  
  if (cleaned.length <= 4) {
    return cleaned;
  } else if (cleaned.length <= 8) {
    return `${cleaned.slice(0, 4)} ${cleaned.slice(4)}`;
  } else if (cleaned.length <= 12) {
    return `${cleaned.slice(0, 4)} ${cleaned.slice(4, 8)} ${cleaned.slice(8)}`;
  } else {
    return `${cleaned.slice(0, 4)} ${cleaned.slice(4, 8)} ${cleaned.slice(8, 12)} ${cleaned.slice(12, 16)}`;
  }
};

/**
 * Validates credit card number using Luhn algorithm
 * Follows Single Responsibility Principle
 */
export const isValidCreditCard = (cardNumber: string): boolean => {
  const cleaned = cardNumber.replace(/\D/g, '');
  
  if (cleaned.length < 13 || cleaned.length > 19) {
    return false;
  }
  
  let sum = 0;
  let isEven = false;
  
  for (let i = cleaned.length - 1; i >= 0; i--) {
    let digit = parseInt(cleaned[i]);
    
    if (isEven) {
      digit *= 2;
      if (digit > 9) {
        digit -= 9;
      }
    }
    
    sum += digit;
    isEven = !isEven;
  }
  
  return sum % 10 === 0;
};

/**
 * Validates US Social Security Number format
 * Follows Single Responsibility Principle
 */
export const isValidSSN = (ssn: string): boolean => {
  const cleaned = ssn.replace(/\D/g, '');
  return cleaned.length === 9 && !/^0{3}|666|9\d{2}/.test(cleaned);
};

/**
 * Formats SSN for display (shows only last 4 digits)
 * Follows Single Responsibility Principle
 */
export const formatSSN = (ssn: string): string => {
  const cleaned = ssn.replace(/\D/g, '');
  
  if (cleaned.length === 9) {
    return `***-**-${cleaned.slice(-4)}`;
  }
  
  return ssn;
};

/**
 * Validates and formats time
 * Follows Single Responsibility Principle
 */
export const formatTime = (time: string): string => {
  const [hours, minutes] = time.split(':').map(Number);
  
  if (isNaN(hours) || isNaN(minutes)) {
    return time;
  }
  
  const period = hours >= 12 ? 'PM' : 'AM';
  const displayHours = hours % 12 || 12;
  const displayMinutes = minutes.toString().padStart(2, '0');
  
  return `${displayHours}:${displayMinutes} ${period}`;
};

/**
 * Validates time format (HH:MM)
 * Follows Single Responsibility Principle
 */
export const isValidTime = (time: string): boolean => {
  const timeRegex = /^([01]?[0-9]|2[0-3]):[0-5][0-9]$/;
  return timeRegex.test(time);
};

/**
 * Validates date range (start date must be before end date)
 * Follows Single Responsibility Principle
 */
export const isValidDateRange = (startDate: string, endDate: string): boolean => {
  const start = new Date(startDate);
  const end = new Date(endDate);
  
  return !isNaN(start.getTime()) && !isNaN(end.getTime()) && start < end;
};

/**
 * Gets validation error message for a field
 * Follows Single Responsibility Principle
 */
export const getFieldError = (errors: FieldValidation, fieldName: string): string => {
  return errors[fieldName]?.message || '';
};

/**
 * Checks if a field has validation errors
 * Follows Single Responsibility Principle
 */
export const hasFieldError = (errors: FieldValidation, fieldName: string): boolean => {
  return !!errors[fieldName] && !errors[fieldName].isValid;
};

/**
 * Clears validation errors for a specific field
 * Follows Single Responsibility Principle
 */
export const clearFieldError = (errors: FieldValidation, fieldName: string): FieldValidation => {
  const newErrors = { ...errors };
  delete newErrors[fieldName];
  return newErrors;
};

/**
 * Clears all validation errors
 * Follows Single Responsibility Principle
 */
export const clearAllErrors = (): FieldValidation => {
  return {};
}; 