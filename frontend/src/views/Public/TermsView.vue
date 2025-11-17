<template>
  <MainLayout>
    <main class="container mx-auto px-4 py-16 sm:py-24 text-white">
      <h1 class="font-display font-bold uppercase text-4xl sm:text-5xl mb-12">
        {{ t('footer.links.terms') }}
      </h1>
      
      <div class="max-w-3xl mx-auto space-y-6 text-gray-300">
        
        <p class="text-gray-500">Última actualización: 17 de noviembre de 2025</p>

        <section>
          <h2 class="font-bold text-xl text-white mb-2">1. Datos Identificativos (Aviso Legal)</h2>
          <p>
            En cumplimiento de la Ley 34/2002, de 11 de julio, de Servicios de la Sociedad de la Información y de Comercio Electrónico (LSSI), te informamos:
          </p>
          <ul class="list-disc list-inside ml-4">
            <li><strong>Titular del Dominio:</strong> A Fervenza Tinta</li>
            <li><strong>NIF:</strong> [Tu NIF/CIF]</li>
            <li><strong>Domicilio Social:</strong> [Tu Dirección Fiscal Completa]</li>
            <li><strong>Email de Contacto:</strong> afervenzatinta@afervenzatinta.com</li>
            </ul>
        </section>

        <section>
          <h2 class="font-bold text-xl text-white mb-2">2. Objeto y Ámbito de Aplicación</h2>
          <p>
            Los presentes Términos y Condiciones (en adelante, "Términos") regulan el acceso, navegación y uso del sitio web afervenzatinta.com (en adelante, la "Plataforma"), así como las responsabilidades derivadas de la utilización de sus contenidos (textos, gráficos, código, etc.).
          </p>
        </section>

        <section>
          <h2 class="font-bold text-xl text-white mb-2">3. Condiciones de Acceso y Registro</h2>
          <p>
            El acceso a la web pública es libre. Sin embargo, el acceso a las funcionalidades privadas (el "Dashboard") requiere un proceso de registro.
          </p>
          <ul class="list-disc list-inside ml-4">
            <li>El usuario debe proporcionar datos veraces (email, teléfono, nombre) memory)].</li>
            <li>El usuario debe verificar su dirección de email.</li>
            <li>El alta definitiva en la plataforma **requiere la aprobación manual por parte de un administrador** . El Titular se reserva el derecho de admisión a la plataforma.</li>
            <li>El usuario es responsable de la custodia de su contraseña.</li>
          </ul>
        </section>

        <section>
          <h2 class="font-bold text-xl text-white mb-2">4. Condiciones de Contratación (Cuotas y Pedidos)</h2>
          <p>
            La plataforma facilita la gestión de cuotas de socio y la compra de merchandising.
          </p>
          <ul class="list-disc list-inside ml-4">
            <li><strong>Cuotas:</strong> El pago de la cuota de socio se realiza a través de la plataforma y es necesario para mantener la condición de socio activo (si aplica).</li>
            <li><strong>Pedidos de Merchandising:</strong> Los usuarios pueden adquirir productos a través de la tienda ("Tenda de Merchandising").</li>
            <li><strong>Métodos de Pago:</strong> Los pagos con tarjeta se procesan de forma segura a través de nuestro proveedor **Stripe**. Los pedidos también pueden ser marcados como "Encargo" para su gestión y pago manual, según se coordine con la administración.</li>
            <li><strong>Precios:</strong> Los precios se indican en Euros (€) e incluyen los impuestos aplicables, salvo que se indique lo contrario.</li>
            </ul>
        </section>

        <section>
          <h2 class="font-bold text-xl text-white mb-2">5. Propiedad Intelectual e Industrial</h2>
          <p>
            El Titular es propietario de todos los derechos de propiedad intelectual e industrial de la Plataforma, su código fuente, diseño gráfico, logotipos (ej. "A Fervenza Tinta") y contenidos. Queda prohibida la reproducción, distribución o transformación no autorizada de dichos elementos.
          </p>
        </section>
        
        <section>
          <h2 class="font-bold text-xl text-white mb-2">6. Exclusión de Responsabilidad</h2>
          <p>
            El Titular no se hace responsable de las caídas del servicio, interrupciones o fallos de los proveedores de terceros (como Stripe, Cloudinary o el proveedor de hosting). El uso de la plataforma es bajo la exclusiva responsabilidad del usuario.
          </p>
        </section>
        
        <section>
          <h2 class="font-bold text-xl text-white mb-2">7. Legislación Aplicable y Jurisdicción</h2>
          <p>
            Estos Términos se rigen por la legislación española. Para cualquier controversia que pudiera derivarse de la aplicación o interpretación de los mismos, las partes se someten a los Juzgados y Tribunales de la ciudad de Vigo, renunciando a cualquier otro fuero que pudiera corresponderles.
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