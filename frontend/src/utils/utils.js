import { COMMON_CONFIG } from '../config/appConfig'

/**
 * Validates a name input
 * @param {string} name - The name string to validate
 * @returns {Object} - { isValid: boolean, errorMessage: string }
 */
export function validName(name) {
    // Check if name is empty or only whitespace
    if (name.trim() === '') {
      return {
        isValid: false,
        errorMessage: ''
      };
    }
  
    // Check if name begins with empty spaces
    if (name[0] === ' ') {
      return {
        isValid: false,
        errorMessage: COMMON_CONFIG.validation.name["leadingSpace"]
      };
    }
  
    // Check if name ends with empty spaces
    if (name[name.length - 1] === ' ') {
      return {
        isValid: false,
        errorMessage: COMMON_CONFIG.validation.name["trailingSpace"]
      };
    }
  
    // Check if name is too short (less than 2 characters)
    if (name.trim().length < 2) {
      return {
        isValid: false,
        errorMessage:  COMMON_CONFIG.validation.name["tooShort"]
      };
    }
  
    // Check if name is too long (more than 50 characters)
    if (name.length > 50) {
      return {
        isValid: false,
        errorMessage: COMMON_CONFIG.validation.name["tooLong"]
      };
    }
  
    // Check if name contains numbers
    if (/\d/.test(name)) {
      return {
        isValid: false,
        errorMessage: COMMON_CONFIG.validation.name["containsNumbers"]
      };
    }
  
    // Check if name contains special characters (except spaces, hyphens, apostrophes, and unicode letters)
    // \p{L} matches any Unicode letter (Latin, Chinese, Arabic, etc.)
    // \p{M} matches combining marks (accents, diacritics)
    if (!/^[\p{L}\p{M}\s\-']+$/u.test(name)) {
      return {
        isValid: false,
        errorMessage: COMMON_CONFIG.validation.name["invalidCharacters"]
      };
    }
  
    // Check if name contains multiple consecutive spaces
    if (/\s{2,}/.test(name)) {
      return {
        isValid: false,
        errorMessage: COMMON_CONFIG.validation.name["multipleSpaces"]
      };
    }
  
    // Check if name starts with a hyphen or apostrophe
    if (/^[-']/.test(name)) {
      return {
        isValid: false,
        errorMessage: COMMON_CONFIG.validation.name["startsWithSpecial"]
      };
    }
  
    // Check if name ends with a hyphen or apostrophe
    if (/[-']$/.test(name)) {
      return {
        isValid: false,
        errorMessage: COMMON_CONFIG.validation.name["endsWithSpecial"]
      };
    }
  
    // Name is valid
    return {
      isValid: true,
      errorMessage: ''
    };
  }