const fs = require('fs');
const path = require('path');

const languages = ['pt', 'fr', 'de', 'ja', 'ko', 'zh'];
const ranges = [
    { name: '0-5', count: 6 },
    { name: '6-10', count: 5 },
    { name: '11-15', count: 5 },
    { name: '16-21', count: 6 }
];
const dataDir = '/home/star/star/public/data';

let allValid = true;

console.log('Starting Verification...');

languages.forEach(lang => {
    console.log(`\nVerifying language: ${lang}`);
    ranges.forEach(range => {
        const filename = `${range.name}_${lang}.json`;
        const filePath = path.join(dataDir, filename);

        if (!fs.existsSync(filePath)) {
            console.error(`❌ Missing file: ${filename}`);
            allValid = false;
            return;
        }

        try {
            const content = fs.readFileSync(filePath, 'utf8');
            const json = JSON.parse(content);

            if (!Array.isArray(json)) {
                console.error(`❌ ${filename} is not an array.`);
                allValid = false;
                return;
            }

            if (json.length !== range.count) {
                console.error(`❌ ${filename} has ${json.length} cards, expected ${range.count}.`);
                allValid = false;
                return;
            }

            // Check for critical fields in the first card as a sample
            const sample = json[0];
            if (!sample.nombre || !sample.contenido || !sample.contenido.arquetipo) {
                console.error(`❌ ${filename} seems to have missing fields in the first card.`);
                allValid = false;
                return;
            }

            console.log(`✅ ${filename} passed.`);

        } catch (e) {
            console.error(`❌ ${filename} is invalid JSON: ${e.message}`);
            allValid = false;
        }
    });
});

if (allValid) {
    console.log('\n✨ All files verified successfully!');
} else {
    console.log('\n⚠️ Some files failed verification.');
    process.exit(1);
}
