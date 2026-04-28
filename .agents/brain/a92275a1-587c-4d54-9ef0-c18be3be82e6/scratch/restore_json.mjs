import fs from 'fs';
import path from 'path';

const entitiesDir = 'downloaded_patents/dv5_special';
const outputJson = '.agents/harness/data/dv5_purified_patents_with_claims.json';

function restoreJson() {
    console.log("Restoring JSON from solidified entity files...");
    const files = fs.readdirSync(entitiesDir).filter(f => f.endsWith('.md'));
    const patents = [];

    files.forEach(file => {
        const content = fs.readFileSync(path.join(entitiesDir, file), 'utf8');
        
        // Simple regex to extract metadata
        const titleMatch = content.match(/- \*\*Title\*\*: (.*)/);
        const dateMatch = content.match(/- \*\*Date\*\*: (.*)/);
        const cpcMatch = content.match(/- \*\*CPC\*\*: (.*)/);
        const tagsMatch = content.match(/- \*\*Tags\*\*: (.*)/);
        const lensIdMatch = content.match(/- \*\*Lens ID\*\*: (.*)/);

        // Extract Abstract and Claims sections
        const abstract = content.split('## Abstract\n')[1]?.split('\n\n## Claims')[0] || '';
        const claims = content.split('## Claims\n')[1]?.split('\n\n## Detailed Description')[0] || '';

        patents.push({
            pub_key: file.replace('.md', ''),
            title: titleMatch?.[1] || 'N/A',
            date: dateMatch?.[1] || 'N/A',
            cpc: cpcMatch?.[1] || 'N/A',
            tags: tagsMatch?.[1] || 'N/A',
            lens_id: lensIdMatch?.[1] || 'N/A',
            abstract: abstract.trim(),
            claims: claims.trim()
        });
    });

    fs.writeFileSync(outputJson, JSON.stringify({ data: patents }, null, 2));
    console.log(`Successfully restored ${patents.length} patents to ${outputJson}`);
}

restoreJson();
