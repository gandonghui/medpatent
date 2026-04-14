import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { join } from 'path';

const resultsFile = 'search_results.json';
const outputDir = 'downloaded_patents';

if (!existsSync(outputDir)) {
    mkdirSync(outputDir, { recursive: true });
}

let data;
try {
    let rawData = readFileSync(resultsFile, 'utf-8');
    // Strip BOM if present
    if (rawData.charCodeAt(0) === 0xFEFF) {
        rawData = rawData.slice(1);
    }
    data = JSON.parse(rawData);
    if (!data.success || !data.results) {
        console.error('Error: Search failed or no results found.');
        process.exit(1);
    }

    data.results.forEach((patent, index) => {
        // Extract a clean filename from patent number or title
        const patentNumber = patent.bibliographic_data?.patent_number || `patent_${index + 1}`;
        const fileName = `${patentNumber.replace(/[^a-z0-9]/gi, '_').toLowerCase()}.md`;
        const filePath = join(outputDir, fileName);

        let content = `# Patent: ${patent.bibliographic_data?.title || 'Unknown Title'}\n\n`;
        content += `## Bibliographic Information\n`;
        content += `- **Patent Number**: ${patent.bibliographic_data?.patent_number || 'N/A'}\n`;
        content += `- **Publication Date**: ${patent.bibliographic_data?.publication_date || 'N/A'}\n`;
        content += `- **Filing Date**: ${patent.bibliographic_data?.filing_date || 'N/A'}\n`;
        content += `- **URL**: [Google Patents](${patent.url || '#'})\n\n`;
        
        content += `## Content\n\n`;
        content += `${patent.content || 'No full content available.'}\n`;

        writeFileSync(filePath, content);
        console.log(`Saved: ${filePath}`);
    });

} catch (e) {
    console.error(`An error occurred: ${e.message}`);
    process.exit(1);
}
