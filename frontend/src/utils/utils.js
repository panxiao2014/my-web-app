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
        errorMessage: 'Name should not begin with empty spaces'
      };
    }
  
    // Check if name ends with empty spaces
    if (name[name.length - 1] === ' ') {
      return {
        isValid: false,
        errorMessage: 'Name should not end with empty spaces'
      };
    }
  
    // Check if name contains only spaces
    if (name.trim().length === 0) {
      return {
        isValid: false,
        errorMessage: 'Name cannot contain only spaces'
      };
    }
  
    // Check if name is too short (less than 2 characters)
    if (name.trim().length < 2) {
      return {
        isValid: false,
        errorMessage: 'Name must be at least 2 characters long'
      };
    }
  
    // Check if name is too long (more than 50 characters)
    if (name.length > 50) {
      return {
        isValid: false,
        errorMessage: 'Name must not exceed 50 characters'
      };
    }
  
    // Check if name contains numbers
    if (/\d/.test(name)) {
      return {
        isValid: false,
        errorMessage: 'Name should not contain numbers'
      };
    }
  
    // Check if name contains special characters (except spaces, hyphens, apostrophes, and unicode letters)
    // \p{L} matches any Unicode letter (Latin, Chinese, Arabic, etc.)
    // \p{M} matches combining marks (accents, diacritics)
    if (!/^[\p{L}\p{M}\s\-']+$/u.test(name)) {
      return {
        isValid: false,
        errorMessage: 'Name should only contain letters, spaces, hyphens, and apostrophes'
      };
    }
  
    // Check if name contains multiple consecutive spaces
    if (/\s{2,}/.test(name)) {
      return {
        isValid: false,
        errorMessage: 'Name should not contain multiple consecutive spaces'
      };
    }
  
    // Check if name starts with a hyphen or apostrophe
    if (/^[-']/.test(name)) {
      return {
        isValid: false,
        errorMessage: 'Name should not start with a hyphen or apostrophe'
      };
    }
  
    // Check if name ends with a hyphen or apostrophe
    if (/[-']$/.test(name)) {
      return {
        isValid: false,
        errorMessage: 'Name should not end with a hyphen or apostrophe'
      };
    }
  
    // Name is valid
    return {
      isValid: true,
      errorMessage: ''
    };
  }