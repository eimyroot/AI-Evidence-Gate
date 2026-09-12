import {test,expect} from '@playwright/test';

test('český přehled vysvětlí smysl produktu',async({page})=>{await page.goto('/');await expect(page.getByText('Ověřte AI změnu dřív, než ji pustíte do provozu.')).toBeVisible();await expect(page.getByText('Vyberete proces')).toBeVisible();await expect(page.getByRole('button',{name:/Spustit novou kontrolu/})).toBeVisible();});

test('jednoduchá kontrola vytvoří srozumitelný výsledek',async({page})=>{await page.goto('/run');await expect(page.getByText('Co chcete ověřit?')).toBeVisible();await page.getByTestId('simple-run').click();await expect(page.getByText(/Prošlo kontrolou|Potřebuje lidskou kontrolu|Nenasazovat/).first()).toBeVisible({timeout:15000});await expect(page.getByText('Proč systém rozhodl právě takto?')).toBeVisible();});

test('rozhodnutí o nasazení vysvětlí druhý krok',async({page})=>{await page.goto('/release-center');await expect(page.getByText('Rozhodnutí o nasazení')).toBeVisible();await expect(page.getByText('Kontrola odpovídá na „jak si nová varianta vedla“.')).toBeVisible();await expect(page.getByRole('button',{name:'Vytvořit rozhodnutí'})).toBeVisible();});

test('jak to funguje používá lidský jazyk',async({page})=>{await page.goto('/jak-to-funguje');await expect(page.getByText('Jak to celé funguje')).toBeVisible();await expect(page.getByText('Obě varianty dostanou stejné testovací případy')).toBeVisible();await expect(page.getByText(/Levnější chyba je pořád chyba/)).toBeVisible();});
