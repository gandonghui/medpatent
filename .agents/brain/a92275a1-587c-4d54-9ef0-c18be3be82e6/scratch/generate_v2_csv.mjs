import fs from 'fs';
import path from 'path';

const entitiesDir = 'downloaded_patents/dv5_special';
const outputCsv = 'doc/analysis/dv5_patents_summary_v2.csv';

function generateEnhancedCsv() {
    console.log("Generating Enhanced CSV (V2) with Claim counts and Jurisdiction...");
    const files = fs.readdirSync(entitiesDir).filter(f => f.endsWith('.md'));
    
    let csv = "lens_id,pub_key,jurisdiction,date_published,title,cpc_codes,claim_count,independent_claim_count,has_full_text,tags\n";

    files.forEach(file => {
        const content = fs.readFileSync(path.join(entitiesDir, file), 'utf8');
        
        const pub_key = file.replace('.md', '');
        const jurisdiction = pub_key.substring(0, 2).replace(/[0-9]/g, '');
        
        const titleMatch = content.match(/- \*\*Title\*\*: (.*)/);
        const dateMatch = content.match(/- \*\*Date\*\*: (.*)/);
        // Corrected regex for CPC
        const cpcMatch = content.match(/- \*\*CPC\*\*: (.*)/);
        const lensIdMatch = content.match(/- \*\*Lens ID\*\*: (.*)/);
        const tagsMatch = content.match(/- \*\*Tags\*\*: (.*)/);

        const claimsSection = content.split('## Claims\n')[1]?.split('\n\n## Detailed Description')[0] || '';
        const claims = claimsSection.split('\n').filter(line => line.trim().length > 10);
        const claimCount = claims.length;
        
        // Simple heuristic for independent claims (lines that don't refer to other claims)
        const indClaimCount = claims.filter(c => !c.toLowerCase().includes('claim 1') && !c.toLowerCase().includes('according to')).length || (claimCount > 0 ? 1 : 0);

        const hasFullText = content.includes('Full Description not fetched') ? 'No' : 'Yes';

        const title = (titleMatch?.[1] || 'N/A').replace(/"/g, '\"');
        const cpc = (cpcMatch?.[1] || 'N/A').replace(/"/g, '\"');

        csv += `"${lensIdMatch?.[1] || ''}","${pub_key}","${jurisdiction}","${dateMatch?.[1] || ''}","${title}","${cpc}",${claimCount},${indClaimCount},"${hasFullText}","${tagsMatch?.[1] || ''}"\n`;
    });

    fs.writeFileSync(outputCsv, csv);
    console.log(`Enhanced CSV generated at ${outputCsv}`);
}

generateEnhancedCsv();
