// Script temporaire pour corriger les événements Enter
const content = `
// Remplacer tous les if (e.key === 'Enter') performHomeSearch(); par if (e.key === 'Enter' && globalEnterToSend.checked) performHomeSearch();
`;