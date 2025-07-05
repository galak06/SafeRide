import {
  validationRules,
  isValidEmail,
  isValidPhone,
  isValidZipCode,
  formatPhoneNumber,
  formatCurrency,
  formatCreditCard,
  isValidCreditCard,
  isValidTime
} from '../../utils/validation';

describe('Validation Utilities', () => {
  describe('Validation Rules', () => {
    describe('required', () => {
      test('passes for non-empty string', () => {
        const rule = validationRules.required('Name');
        expect(rule.test('John')).toBe(true);
        expect(rule.message).toBe('Name is required');
      });

      test('fails for empty string', () => {
        const rule = validationRules.required('Name');
        expect(rule.test('')).toBe(false);
      });

      test('fails for whitespace-only string', () => {
        const rule = validationRules.required('Name');
        expect(rule.test('   ')).toBe(false);
      });
    });

    describe('email', () => {
      test('passes for valid email addresses', () => {
        const rule = validationRules.email();
        expect(rule.test('test@example.com')).toBe(true);
        expect(rule.test('user.name+tag@domain.co.uk')).toBe(true);
        expect(rule.test('123@456.789')).toBe(true);
      });
    });

    describe('phone', () => {
      test('passes for valid phone numbers', () => {
        const rule = validationRules.phone();
        expect(rule.test('1234567890')).toBe(true);
        expect(rule.test('(123) 456-7890')).toBe(true);
        expect(rule.test('123-456-7890')).toBe(true);
        expect(rule.test('+1 123 456 7890')).toBe(true);
      });

      test('fails for invalid phone numbers', () => {
        const rule = validationRules.phone();
        expect(rule.test('123')).toBe(false);
        expect(rule.test('123456789')).toBe(false);
        expect(rule.test('abc-def-ghij')).toBe(false);
      });
    });

    describe('passwordConfirm', () => {
      test('passes when passwords match', () => {
        const rule = validationRules.passwordConfirm('Password123!');
        expect(rule.test('Password123!')).toBe(true);
      });

      test('fails when passwords do not match', () => {
        const rule = validationRules.passwordConfirm('Password123!');
        expect(rule.test('DifferentPassword123!')).toBe(false);
      });
    });

    describe('minLength', () => {
      test('passes for strings with sufficient length', () => {
        const rule = validationRules.minLength(5);
        expect(rule.test('Hello')).toBe(true);
        expect(rule.test('Hello World')).toBe(true);
      });

      test('fails for strings that are too short', () => {
        const rule = validationRules.minLength(5);
        expect(rule.test('Hi')).toBe(false);
        expect(rule.test('')).toBe(false);
      });
    });

    describe('zipCode', () => {
      test('passes for valid ZIP codes', () => {
        const rule = validationRules.zipCode();
        expect(rule.test('12345')).toBe(true);
        expect(rule.test('12345-6789')).toBe(true);
      });

      test('fails for invalid ZIP codes', () => {
        const rule = validationRules.zipCode();
        expect(rule.test('1234')).toBe(false); // Too short
        expect(rule.test('123456')).toBe(false); // Too long
        expect(rule.test('12345-678')).toBe(false); // Invalid format
        expect(rule.test('abcde')).toBe(false); // Non-numeric
      });
    });

    describe('numeric', () => {
      test('passes for numeric strings', () => {
        const rule = validationRules.numeric();
        expect(rule.test('123')).toBe(true);
        expect(rule.test('0')).toBe(true);
        expect(rule.test('999999')).toBe(true);
      });

      test('fails for non-numeric strings', () => {
        const rule = validationRules.numeric();
        expect(rule.test('123a')).toBe(false);
        expect(rule.test('abc')).toBe(false);
        expect(rule.test('12.34')).toBe(false);
        expect(rule.test('')).toBe(false);
      });
    });

    describe('positiveNumber', () => {
      test('passes for positive numbers', () => {
        const rule = validationRules.positiveNumber();
        expect(rule.test('1')).toBe(true);
        expect(rule.test('123.45')).toBe(true);
        expect(rule.test('0.1')).toBe(true);
      });

      test('fails for non-positive numbers', () => {
        const rule = validationRules.positiveNumber();
        expect(rule.test('0')).toBe(false);
        expect(rule.test('-1')).toBe(false);
        expect(rule.test('-123.45')).toBe(false);
      });
    });
  });

  describe('Utility Functions', () => {
    describe('isValidEmail', () => {
      test('returns true for valid emails', () => {
        expect(isValidEmail('test@example.com')).toBe(true);
        expect(isValidEmail('user.name+tag@domain.co.uk')).toBe(true);
      });

      test('returns false for invalid emails', () => {
        expect(isValidEmail('invalid-email')).toBe(false);
        expect(isValidEmail('test@')).toBe(false);
        expect(isValidEmail('@example.com')).toBe(false);
      });
    });

    describe('isValidPhone', () => {
      test('returns true for valid phone numbers', () => {
        expect(isValidPhone('1234567890')).toBe(true);
        expect(isValidPhone('(123) 456-7890')).toBe(true);
        expect(isValidPhone('123-456-7890')).toBe(true);
      });

      test('returns false for invalid phone numbers', () => {
        expect(isValidPhone('123')).toBe(false);
        expect(isValidPhone('123456789')).toBe(false);
        expect(isValidPhone('abc-def-ghij')).toBe(false);
      });
    });

    describe('isValidZipCode', () => {
      test('returns true for valid ZIP codes', () => {
        expect(isValidZipCode('12345')).toBe(true);
        expect(isValidZipCode('12345-6789')).toBe(true);
      });

      test('returns false for invalid ZIP codes', () => {
        expect(isValidZipCode('1234')).toBe(false);
        expect(isValidZipCode('123456')).toBe(false);
        expect(isValidZipCode('abcde')).toBe(false);
      });
    });

    describe('formatPhoneNumber', () => {
      test('formats 10-digit numbers', () => {
        expect(formatPhoneNumber('1234567890')).toBe('(123) 456-7890');
      });

      test('handles already formatted numbers', () => {
        expect(formatPhoneNumber('(123) 456-7890')).toBe('(123) 456-7890');
      });

      test('handles invalid input', () => {
        expect(formatPhoneNumber('123')).toBe('123');
        expect(formatPhoneNumber('')).toBe('');
      });
    });

    describe('formatCurrency', () => {
      test('formats currency values', () => {
        expect(formatCurrency(1234.56)).toBe('$1,234.56');
        expect(formatCurrency(0)).toBe('$0.00');
        expect(formatCurrency(1000000)).toBe('$1,000,000.00');
      });

      test('handles negative values', () => {
        expect(formatCurrency(-1234.56)).toBe('-$1,234.56');
      });
    });

    describe('formatCreditCard', () => {
      test('formats credit card numbers', () => {
        expect(formatCreditCard('1234567890123456')).toBe('1234 5678 9012 3456');
        expect(formatCreditCard('123456789012345')).toBe('1234 5678 9012 345');
      });

      test('handles short numbers', () => {
        expect(formatCreditCard('1234')).toBe('1234');
        expect(formatCreditCard('')).toBe('');
      });
    });

    describe('isValidCreditCard', () => {
      test('validates credit card numbers', () => {
        expect(isValidCreditCard('4532015112830366')).toBe(true); // Visa
        expect(isValidCreditCard('5555555555554444')).toBe(true); // Mastercard
        expect(isValidCreditCard('378282246310005')).toBe(true); // American Express
      });

      test('rejects invalid numbers', () => {
        expect(isValidCreditCard('1234567890123456')).toBe(false);
        expect(isValidCreditCard('1234')).toBe(false);
        expect(isValidCreditCard('')).toBe(false);
      });
    });

    describe('isValidTime', () => {
      test('validates time format', () => {
        expect(isValidTime('12:00')).toBe(true);
        expect(isValidTime('23:59')).toBe(true);
        expect(isValidTime('00:00')).toBe(true);
      });

      test('rejects invalid time', () => {
        expect(isValidTime('24:00')).toBe(false);
        expect(isValidTime('12:60')).toBe(false);
        expect(isValidTime('25:30')).toBe(false);
        expect(isValidTime('12:00:00')).toBe(false);
      });
    });
  });
}); 