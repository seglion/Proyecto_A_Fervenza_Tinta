<template>
  <MainLayout>
    <main class="container mx-auto px-4 py-16 sm:py-24 text-white">
      <h1 class="font-display font-bold uppercase text-4xl sm:text-5xl mb-12">
        {{ t('footer.links.privacy') }}
      </h1>
      
      <div class="max-w-3xl mx-auto space-y-6 text-gray-300">
        
        <p class="text-gray-500">Última actualización: 17 de noviembre de 2025</p>

        <section>
          <h2 class="font-bold text-xl text-white mb-2">1. Responsable del Tratamiento</h2>
          <p>
            El responsable del tratamiento de los datos recabados a través de este sitio web es:
          </p>
          <ul class="list-disc list-inside ml-4">
            <li><strong>Titular:</strong> Asociación A Fervenza Tinta</li>
            <li><strong>NIF:</strong> [Tu NIF/CIF]</li>
            <li><strong>Domicilio Social:</strong> [Tu Dirección Fiscal Completa]</li>
            
          </ul>
        </section>

        <section>
          <h2 class="font-bold text-xl text-white mb-2">2. Qué Datos Recopilamos</h2>
          <p>
            Recopilamos los siguientes datos personales que nos proporcionas directamente:
          </p>
          <ul class="list-disc list-inside ml-4">
            <li><strong>Datos de Registro:</strong> Nombre, apellidos, dirección de email, número de teléfono.</li>
            <li><strong>Datos de Perfil :</strong> Fotografía de perfil (avatar) ].</li>
            <li><strong>Datos de Autenticación:</strong> Contraseña hasheada (nunca almacenamos tu contraseña en texto plano).</li>
            <li><strong>Datos de Pago:</strong> NO almacenamos los datos de tu tarjeta de crédito. Esta información es gestionada de forma segura y directa por nuestro proveedor de pagos, Stripe. Solo almacenamos un registro de la transacción (importe, fecha, método de pago).</li>
            <li><strong>Imágenes Subidas:</strong> Si subes una foto de perfil, esta se almacena de forma segura en nuestro proveedor de alojamiento de archivos (Cloudinary).</li>
          </ul>
        </section>

        <section>
          <h2 class="font-bold text-xl text-white mb-2">3. Finalidad del Tratamiento</h2>
          <p>
            Usamos tus datos para las siguientes finalidades:
          </p>
          <ul class="list-disc list-inside ml-4">
            <li>Gestionar tu alta y acceso como usuario registrado a la plataforma.</li>
            <li>Validar tu cuenta mediante la verificación de email.</li>
            <li>Permitir a los administradores aprobar tu acceso a la aplicación.</li>
            <li>Procesar el pago de tus cuotas de socio y pedidos de merchandising.</li>
            <li>Gestionar la logística de los pedidos encargados.</li>
            <li>Permitir la recuperación de tu contraseña.</li>
          </ul>
        </section>

        <section>
          <h2 class="font-bold text-xl text-white mb-2">4. Legitimación</h2>
          <p>
            La base legal para el tratamiento de tus datos es:
          </p>
          <ul class="list-disc list-inside ml-4">
            <li>La **ejecución de un contrato** (los Términos y Condiciones) para prestarte el servicio, gestionar tus pagos y pedidos.</li>
          </ul>
        </section>

        <section>
          <h2 class="font-bold text-xl text-white mb-2">5. Destinatarios (Cesión de Datos)</h2>
          <p>
            No cederemos tus datos a terceros, salvo obligación legal. Sin embargo, para operar, utilizamos proveedores de servicios que pueden tener acceso a tus datos (actuando como Encargados del Tratamiento):
          </p>
          <ul class="list-disc list-inside ml-4">
            <li><strong>Stripe, Inc.:</strong> Para el procesamiento de pagos seguros con tarjeta.</li>
            <li><strong>Cloudinary, Inc.:</strong> Para el almacenamiento de las imágenes de perfil (avatar) y prendas.</li>
            <li><strong>Sendgrid</strong> Para el envío de emails transaccionales (verificación, reseteo de contraseña).</li>
            <li><strong>Hetzner:</strong> Donde se aloja nuestra base de datos.</li>
          </ul>
        </section>

        <section>
          <h2 class="font-bold text-xl text-white mb-2">6. Tus Derechos (ARCO-POL)</h2>
          <p>
            Puedes ejercer tus derechos de Acceso, Rectificación, Cancelación (Supresión), Oposición, Limitación del Tratamiento y Portabilidad de tus datos enviando un email a afervenzatinta@afervenzatina.com, adjuntando una copia de tu DNI.
          </p>
        </section>

        <section>
          <h2 class="font-bold text-xl text-white mb-2">7. Plazo de Conservación</h2>
          <p>
            Conservaremos tus datos mientras seas usuario activo de la plataforma. Una vez solicites la baja, se conservarán bloqueados únicamente durante el tiempo necesario para cumplir con las obligaciones legales.
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