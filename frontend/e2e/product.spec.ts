import {test,expect} from '@playwright/test';

test('základní režim ukazuje jen hlavní proces',async({page})=>{
 await page.goto('/');
 await expect(page.getByText('Ověřte AI změnu dřív, než ji pustíte do provozu.')).toBeVisible();
 await expect(page.getByRole('link',{name:'Bezpečnost'})).toHaveCount(0);
 await page.getByRole('button',{name:'+ Pokročilé'}).click();
 await expect(page.getByRole('link',{name:'Bezpečnost'})).toBeVisible();
});

test('nová kontrola nevyžaduje technické nastavení',async({page})=>{
 await page.goto('/run');
 await expect(page.getByText('Co chcete ověřit?')).toBeVisible();
 await expect(page.getByText('Kontrolní pravidla')).toHaveCount(0);
 await page.getByRole('button',{name:'Pokročilé nastavení'}).click();
 await expect(page.getByText('Kontrolní pravidla')).toBeVisible();
 await page.getByTestId('simple-run').click();
 await expect(page.getByText(/Prošlo kontrolou|Potřebuje lidskou kontrolu|Nenasazovat/).first()).toBeVisible({timeout:15000});
});

test('výsledek vysvětlí další krok a schová technické detaily',async({page})=>{
 await page.goto('/run');
 await page.getByTestId('simple-run').click();
 await expect(page.getByText('Co dál?')).toBeVisible({timeout:15000});
 await expect(page.getByText('Technické detaily kontroly')).toBeVisible();
 await page.getByText('Technické detaily kontroly').click();
 await expect(page.getByText(/testovaci_sada/)).toBeVisible();
});

test('jak to funguje používá lidský jazyk',async({page})=>{
 await page.goto('/jak-to-funguje');
 await expect(page.getByText('Jak to celé funguje')).toBeVisible();
 await expect(page.getByText('Kontrolní vrstva mezi automatizací a dlouhodobým provozem')).toBeVisible();
 await expect(page.getByRole('main').getByText('AI Evidence Gate',{exact:true})).toBeVisible();
 await expect(page.getByText('Gate není jednorázová kontrola.')).toBeVisible();
 await expect(page.getByText('Obě varianty dostanou stejné testovací případy')).toBeVisible();
 await expect(page.getByText(/Levnější chyba je pořád chyba/)).toBeVisible();
});

test('mobilní layout nemá horizontální overflow',async({page})=>{
 await page.setViewportSize({width:390,height:844});
 for(const path of ['/','/run']){
  await page.goto(path);
  const dims=await page.evaluate(()=>({scrollWidth:document.documentElement.scrollWidth,clientWidth:document.documentElement.clientWidth}));
  expect(dims.scrollWidth).toBe(dims.clientWidth);
 }
});
