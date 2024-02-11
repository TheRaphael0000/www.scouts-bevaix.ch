Fancybox.bind('[data-fancybox="gallery"]', {
  on: {
    "Carousel.change": update_backdrop,
    "Carousel.ready": update_backdrop,
    // "*": (carousel, eventName) => {
    //   console.log(`Carousel eventName: ${eventName}`);
    // },
  },
});

function update_backdrop(instance) {
  const slide = instance.carousel.slides[instance.carousel.page];
  instance.container.style.setProperty(
    "--bg-image",
    `url("${slide.thumbSrc}")`
  );
}