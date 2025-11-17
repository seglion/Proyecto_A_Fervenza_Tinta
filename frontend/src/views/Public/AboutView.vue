<template>
  <MainLayout>
    <main class="container mx-auto px-4 py-16 sm:py-24 text-white">
      
      <h1 class="font-display font-bold uppercase text-4xl sm:text-5xl mb-12 text-center">
        {{ t('footer.links.about') }}
      </h1>
      
      <div class="max-w-3xl mx-auto space-y-8 text-gray-300">

        <section class="text-center">
          <h2 class="font-display text-2xl sm:text-3xl text-brand-red mb-4">
            MÁIS QUE UNHA BANDA, UNHA FAMILIA
          </h2>
          <p class="text-lg">
            "A Fervenza Tinta" é máis ca unha banda; é o símbolo da amizade e da tradición en A Guarda. Nacemos da paixón compartida por unha das festas máis emblemáticas da nosa vila, o <strong>Domingo do Monte</strong>, e medramos co obxectivo de gozalo xuntos.
          </p>
        </section>

        <hr class="border-gray-800">

        <section>
          <h3 class="font-display text-xl sm:text-2xl text-white mb-3">A Nosa Historia: O Comezo (2004)</h3>
          <p>
            A nosa historia comeza no ano 2004. Un grupo de amigos de A Guarda, moitos dos cales xa formaban parte doutras bandas e charangas, decidiron que querían vivir o Domingo do Monte dun xeito diferente: todos xuntos.
          </p>
          <p class="mt-2">
            O que comezou como un desexo de gozar da festa entre compañeiros inseparables, consolidouse rapidamente como a fundación dunha nova e icónica banda. O obxectivo era sinxelo: pasalo ben e facer desfrutar á xente co noso ritmo.
          </p>
        </section>

        <section class="space-y-6">
          <div>
            <h3 class="font-display text-xl sm:text-2xl text-white mb-3">Que significa "A Fervenza Tinta"?</h3>
            <p>
              O noso nome captura a esencia pura da festa. Vén desa imaxe tan guardesa: o <strong>"enxurro" (o chorro) de viño tinto</strong> que baixa pola gorxa cando se leva a cabo a "xura" (o tradicional xuramento de beber) no Monte. É un nome que evoca celebración, paixón e o fluír da festa que tanto nos define.
            </p>
          </div>

          <div>
            <h3 class="font-display text-xl sm:text-2xl text-white mb-3">Os Nosos Sinais de Identidade</h3>
            <p>
              Se nos ves, recoñecerásnos. A nosa cor predominante é o <strong>vermello vivo</strong>, a cor da festa e do viño que nos dá nome. Lucímolo con orgullo na nosa camisa e no noso <strong>faxín</strong>.
            </p>
            <p class="mt-2">
              Este vermello inconfundible contrasta co <strong>negro</strong> dos nosos pantalóns (ou saias), a gorra e a tradicional <strong>pañoleta</strong>, creando unha identidade visual única nas rúas da Guarda.
            </p>
          </div>

          <div>
            <h3 class="font-display text-xl sm:text-2xl text-white mb-3">O Noso Estandarte</h3>
            <p>
              A nosa bandeira é unha homenaxe directa á nosa vila. Simula a bandeira e o escudo de A Guarda, pero co noso toque persoal: sobrepuxemos a imaxe dun festexeiro "xurando" (bebendo) co inconfundible porto de A Guarda como telón de fondo. É a unión da nosa identidade como banda e o noso profundo amor pola nosa terra.
            </p>
          </div>
        </section>

        <hr class="border-gray-800">

        <section>
          <h3 class="font-display text-xl sm:text-2xl text-white mb-3">Un "Toque" Único</h3>
          <p>
            O que nos fai soar diferente é o noso "toque". Esta particularidade musical, o ritmo que define a A Fervenza Tinta, é autoría de dous dos nosos membros fundadores, <strong>Denis e Kiko</strong>. Eles compuxeron a melodía que, ano tras ano, resoa no Monte e convida a todos a unirse á celebración.
          </p>
        </section>

      </div>
    </main>
  </MainLayout>
</template>

<script setup>
import MainLayout from '@/components/Landing/layout/MainLayout.vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
</script>