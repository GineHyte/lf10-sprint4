const FIELD_TYPES = {
    "sex": "radio-button",
    "credit_format": "radio-button",
    "first_name": "text-input",
    "last_name": "text-input",
    "street": "text-input",
    "house_number": "text-input",
    "zip": "number-input",
    "city": "text-input",
    "business_phone": "text-input",
    "private_phone": "text-input",
    "personal_phone": "text-input",
    "email": "text-input",
    "birthday": "date-picker",
    "homeland": "text-input",
    "resident_since_months": "number-input",
    "marital_status": "radio-button",
    "dependent_children": "number-input",
    "current_profession": "text-input",
    "employed_since_months": "number-input",
    "main_employer": "text-input",
    "main_employer_zip": "number-input",
    "main_employer_city": "text-input",
    "main_net_salary": "number-input",
    "main_13th_salary": "radio-button",
    "secondary_employer": "text-input",
    "secondary_employer_zip": "number-input",
    "secondary_employer_city": "text-input",
    "secondary_net_salary": "number-input",
    "secondary_13th_salary": "radio-button",
    "desired_credit_amount": "number-input",
    "credit_duration_months": "number-input",
    "insurance_interest": "radio-button",
    "outstanding_debts": "radio-button",
    "outstanding_debts_details": "text-input",
};

/**
 * Return a synchronous hex string of the requested length using secure random bytes.
 * Example: `randomHex(8)` -> "a3f4b1c2"
 * @param {number} length - number of hex characters to return (positive integer)
 * @returns {string} hex string of length `length`
 */
function randomHex(length = 8) {
    const n = Math.max(0, Math.floor(Number(length) || 0));
    if (n === 0) return '';r
    const bytesNeeded = Math.ceil(n / 2);
    const rnd = crypto.getRandomValues(new Uint8Array(bytesNeeded));
    const hex = Array.from(rnd).map(b => b.toString(16).padStart(2, '0')).join('');
    return hex.slice(0, n);
}

function getFieldType(field) { // TODO: move this function to backend
    return FIELD_TYPES[field]
}